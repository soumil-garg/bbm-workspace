"""Model-based theme counter (Stage 2 / 3b). Replaces keyword regex counts with yes/no questions answered by Jev (TypeSafe, counter) and Luna (OpenAI Decisions, second reader).
Rules for writing the questions: references/theme-question-rules.md. Worked example: references/theme-questions-example-habbits.json.

  python theme_counter.py --reviews reviews.json --themes themes.json --out OUTDIR [--limit N] [--no-second] [--luna-skip a,b] [--audit 100]

reviews.json: Amazon pull {product: [{"s": "1".."5", "t": title, "b": body}, ...]} or a list of {"product","stars","text"} or {"id","text"}.
themes.json:  {"theme_name": "Does the reviewer say ...? Answer no if ..."}.
Keys come from the user environment (never printed): TYPESAFE_API_KEY (Jev), OPENAI_API_KEY (Luna). Public text only; PII is stripped before anything leaves the machine.
Outputs in OUTDIR:
  theme_counts.md      per theme: yes count by Jev, share with Wilson 95% interval (all reviews and 1-3 star), flagged answers, range if the flagged answers are resolved either way
  theme_answers.json   per review per theme: Jev and Luna probabilities
  flagged.md/.json     answers for a second reader (Jev in 0.25-0.75, Jev and Luna disagree, Luna refused)
  samples_<theme>.txt  up to 25 verbatim texts per theme, highest Jev probability first (uses <theme>_quote_grade when that sibling question exists)
  audit_reviews.json   (--audit N) N random reviews, text only, for the blind audit labellers; audit_manifest.json keeps product/stars
  run_summary.json     tokens, cost, flagged share, seconds
Cost guide (Habbits, 22 questions): Jev about 0.9k tokens per review ($0.04 per 1,000 reviews), Luna about 3.5k tokens per review ($0.35 per 1,000).
"""
import os, sys, json, re, time, math, random, hashlib, argparse, io, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

JEV_MODEL = 'jev-1.13.0'          # pinned on purpose, never jev-latest
JEV_URL = 'https://api.typesafe.ai/v1/systemone'
LUNA_URL = 'https://api.openai.com/v1/decisions'
JEV_PRICE, LUNA_PRICE = 0.042 / 1e6, 0.10 / 1e6


def getenv(name):
    # Registry first (2026-10-10): the user environment variable is the source of truth, so a rotated key takes effect at once;
    # os.environ is only a snapshot from when the parent app started.
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 'Environment') as h:
            v = winreg.QueryValueEx(h, name)[0]
            if v:
                return v
    except Exception:
        pass
    return os.environ.get(name)


def strip_pii(text):
    t = re.sub(r'https?://\S+|www\.\S+', ' ', text or '')
    t = re.sub(r'\S+@\S+', ' ', t)
    t = re.sub(r'(?<!\w)@\w+', ' ', t)
    t = re.sub(r'\+?\d[\d\s\-]{7,}\d', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()


def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    r = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - r) / d, (c + r) / d


def load_rows(path):
    d = json.load(open(path, encoding='utf-8'))
    rows = []
    if isinstance(d, dict):
        for prod, lst in d.items():
            for r in lst:
                if isinstance(r, dict) and 'b' in r:
                    rows.append({'product': prod, 'stars': int(r.get('s') or 0), 'text': strip_pii(((r.get('t') or '') + ' ' + r['b']).strip())})
    else:
        for r in d:
            rows.append({'product': r.get('product', ''), 'stars': int(r.get('stars') or 0), 'text': strip_pii(r.get('text', ''))})
    rows = [r for r in rows if len(r['text']) > 5]
    for i, r in enumerate(rows):
        r['id'] = i
    return rows


class Auth(RuntimeError):
    pass


def post(url, headers, body, tries=6):
    data = json.dumps(body).encode('utf-8')
    last = None
    for a in range(tries):
        req = urllib.request.Request(url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            detail = e.read().decode('utf-8', 'ignore')[:200]
            if e.code in (401, 403):
                raise Auth(f'HTTP {e.code}: {detail}')
            if e.code in (408, 409, 429, 529) or e.code >= 500:
                time.sleep(2 ** a)
                last = f'HTTP {e.code}: {detail}'
                continue
            raise RuntimeError(f'HTTP {e.code}: {detail}')
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            time.sleep(2 ** a)
            last = str(e)
    raise RuntimeError('gave up: ' + str(last))


class Cache:
    def __init__(self, path):
        import threading
        self.lock = threading.Lock()
        self.path, self.d = path, {}
        if os.path.exists(path):
            for line in open(path, encoding='utf-8'):
                try:
                    x = json.loads(line)
                    self.d[x['k']] = x['v']
                except Exception:
                    pass

    def get(self, k):
        return self.d.get(k)

    def put(self, k, v):
        with self.lock:
            self.d[k] = v
            with open(self.path, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'k': k, 'v': v}, ensure_ascii=False) + '\n')


def ask_jev(text, themes, key, cache):
    ck = hashlib.sha256(json.dumps(['jev', JEV_MODEL, text, themes], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    hit = cache.get(ck)
    if hit:
        return hit
    r = post(JEV_URL, {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
             {'state': text, 'model': JEV_MODEL, 'questions': {k: {'type': 'noul', 'instructions': q} for k, q in themes.items()}})
    out = {'p': {k: r['answers'][k]['noul'] for k in themes}, 'tokens': r.get('usage', {}).get('input_tokens', 0)}
    cache.put(ck, out)
    return out


def ask_luna(text, themes, key, cache):
    ck = hashlib.sha256(json.dumps(['luna', text, themes], sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    hit = cache.get(ck)
    if hit:
        return hit
    r = post(LUNA_URL, {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'},
             {'model': 'gpt-6-luna', 'input': text, 'questions': [{'type': 'predicate', 'name': k, 'instructions': q} for k, q in themes.items()]})
    p = {x['name']: (x['probability'] if x['type'] == 'predicate' else None) for x in r['answers']}      # None = refusal ("cannot tell")
    out = {'p': {k: p.get(k) for k in themes}, 'tokens': r.get('usage', {}).get('input_tokens', 0)}
    cache.put(ck, out)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reviews', required=True)
    ap.add_argument('--themes', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--limit', type=int)
    ap.add_argument('--no-second', action='store_true', help='skip Luna (counts only, no second-reader flags)')
    ap.add_argument('--luna-skip', default='compares_other_brand', help='comma list of themes where Luna is not used (its wording broke on these)')
    ap.add_argument('--audit', type=int, default=0, help='also write N random reviews for the blind audit')
    ap.add_argument('--seed', type=int, default=11)
    ap.add_argument('--workers', type=int, default=4, help='parallel calls per model (Jev and Luna each get this many); 10 is fine for long prompts')
    a = ap.parse_args()
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    os.makedirs(a.out, exist_ok=True)
    themes = json.load(open(a.themes, encoding='utf-8'))
    rows = load_rows(a.reviews)
    if a.limit:
        rows = rows[:a.limit]
    jkey = getenv('TYPESAFE_API_KEY')
    lkey = None if a.no_second else getenv('OPENAI_API_KEY')
    if not jkey:
        sys.exit('TYPESAFE_API_KEY not set (user environment variable)')
    if not a.no_second and not lkey:
        sys.exit('OPENAI_API_KEY not set; use --no-second to count with Jev only')
    skip = {s for s in a.luna_skip.split(',') if s}
    jc, lc = Cache(os.path.join(a.out, 'cache_jev.jsonl')), Cache(os.path.join(a.out, 'cache_luna.jsonl'))
    t0 = time.time()
    # Jev and Luna run at the same time, each with its own pool (v2.1: 4 workers took about 85 texts a minute on long Reddit prompts); results are cached, so a re-run resumes
    with ThreadPoolExecutor(a.workers) as exj, ThreadPoolExecutor(a.workers) as exl:
        jf = [exj.submit(ask_jev, r['text'], themes, jkey, jc) for r in rows]
        lf = [exl.submit(ask_luna, r['text'], themes, lkey, lc) for r in rows] if lkey else None
        jres = [f.result() for f in jf]
        lres = [f.result() for f in lf] if lf else [None] * len(rows)
    secs = time.time() - t0
    N = len(rows)
    crit = [i for i, r in enumerate(rows) if 1 <= r['stars'] <= 3]
    answers, flagged = [], []
    yes = {t: [] for t in themes}
    for i, r in enumerate(rows):
        row = {'id': r['id'], 'product': r['product'], 'stars': r['stars'], 'answers': {}}
        for t in themes:
            jp = jres[i]['p'][t]
            lp = lres[i]['p'][t] if lres[i] else None
            row['answers'][t] = {'jev': jp, 'luna': lp}
            if jp >= 0.5:
                yes[t].append(i)
            reason = None
            if 0.25 <= jp <= 0.75:
                reason = 'jev_middle'
            elif lres[i] and t not in skip:
                if lp is None:
                    reason = 'luna_refused'
                elif (lp >= 0.5) != (jp >= 0.5):
                    reason = 'models_disagree'
            if reason:
                flagged.append({'id': r['id'], 'theme': t, 'jev': round(jp, 2), 'luna': None if lp is None else round(lp, 2), 'reason': reason, 'jev_yes': jp >= 0.5, 'text': r['text'][:500]})
        answers.append(row)
    json.dump(answers, open(os.path.join(a.out, 'theme_answers.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(flagged, open(os.path.join(a.out, 'flagged.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    with open(os.path.join(a.out, 'flagged.md'), 'w', encoding='utf-8') as f:
        f.write(f'# Flagged answers for a second reader ({len(flagged)} of {N * len(themes)} answers = {100 * len(flagged) / max(1, N * len(themes)):.1f}%)\n\n')
        for x in flagged:
            f.write(f'- [{x["id"]}] **{x["theme"]}** jev {x["jev"]} luna {x["luna"]} ({x["reason"]}): {x["text"][:300]}\n')
    # counts table
    fl_by = {t: [x for x in flagged if x['theme'] == t] for t in themes}
    lines = [f'# Theme counts (Jev counter, Luna second reader). Reviews: {N}; critical 1-3 star: {len(crit)}.\n',
             'Share = Jev yes / N with Wilson 95% interval. Range = the yes count if every flagged answer for that theme went one way or the other. Never quote a share for a theme the audit has not cleared.\n',
             '| Theme | Yes (all) | Share | 95% interval | Yes (critical) | Share of critical | Flagged | Range (all) |', '|---|---|---|---|---|---|---|---|']
    for t in themes:
        y = len(yes[t])
        lo, hi = wilson(y, N)
        yc = sum(1 for i in yes[t] if i in set(crit))
        flo, fhi = wilson(yc, len(crit)) if crit else (0, 0)
        fy = sum(1 for x in fl_by[t] if x['jev_yes'])
        fn = len(fl_by[t]) - fy
        lines.append(f'| {t} | {y} | {100 * y / N:.1f}% | {100 * lo:.1f}-{100 * hi:.1f}% | {yc} | ' + (f'{100 * yc / len(crit):.1f}% ({100 * flo:.0f}-{100 * fhi:.0f}%)' if crit else '-') + f' | {len(fl_by[t])} | {y - fy}-{y + fn} |')
    open(os.path.join(a.out, 'theme_counts.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    # samples
    for t in themes:
        src = t + '_quote_grade' if (t + '_quote_grade') in themes else t
        ids = sorted([i for i in range(N) if jres[i]['p'][src] >= 0.5], key=lambda i: -jres[i]['p'][src])[:25]
        with open(os.path.join(a.out, f'samples_{t}.txt'), 'w', encoding='utf-8') as f:
            f.write(f'{t} (samples from {src}): {len(yes[t])} yes of {N}\n\n')
            for i in ids:
                f.write(f'[{rows[i]["product"]} {rows[i]["stars"]}*, jev {jres[i]["p"][src]:.2f}] {rows[i]["text"][:600]}\n\n')
    if a.audit:
        random.seed(a.seed)
        pick = random.sample(range(N), min(a.audit, N))
        json.dump([{'id': k, 'text': rows[i]['text']} for k, i in enumerate(pick)], open(os.path.join(a.out, 'audit_reviews.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        json.dump([{'id': k, 'source_id': rows[i]['id'], 'product': rows[i]['product'], 'stars': rows[i]['stars']} for k, i in enumerate(pick)], open(os.path.join(a.out, 'audit_manifest.json'), 'w', encoding='utf-8'), indent=1)
    jt = sum(x['tokens'] for x in jres)
    lt = sum(x['tokens'] for x in lres if x)
    summ = {'reviews': N, 'critical': len(crit), 'themes': len(themes), 'jev_tokens': jt, 'jev_usd': round(jt * JEV_PRICE, 4), 'luna_tokens': lt, 'luna_usd': round(lt * LUNA_PRICE, 4),
            'flagged_answers': len(flagged), 'flagged_pct': round(100 * len(flagged) / max(1, N * len(themes)), 1), 'seconds': round(secs), 'jev_model': JEV_MODEL}
    json.dump(summ, open(os.path.join(a.out, 'run_summary.json'), 'w'), indent=1)
    print(open(os.path.join(a.out, 'theme_counts.md'), encoding='utf-8').read())
    print(json.dumps(summ))


if __name__ == '__main__':
    main()
