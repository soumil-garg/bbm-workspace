"""Count themes in reviews and Reddit text (regex + manual review), so pains are sized by numbers, not by feel.

  python theme_count.py --themes themes.json --amazon amazon_reviews.json [--reddit reddit_threads.json] --out C:/cca/<brand>/research/themes

themes.json: {"doesnt_work": "not work|no result|fake|waste|bakwas", "price": "price|costly|overpriced|expensive", ...}   (regex, case-insensitive)
Inputs:
  --amazon  JSON {product: [{"s": "1".."5", "t": title, "b": body, "f": filter}, ...]} (the shape the Amazon pull script saves)
            or a list of {"product","stars","text"}.
  --reddit  JSON list of {"sub","title","text","score","comments": [[upvotes, text], ...]} (reddit_research.py output).
Outputs in --out:
  theme_counts.md   per theme: reviews matched (all and critical 1-3 star) with % of the critical set, Reddit threads and
                    comments matched, plus per-product split
  samples_<theme>.txt   up to 25 matched texts per theme (READ THESE: remove false matches, tighten the pattern, re-run)
  unmatched_critical.txt   25 critical reviews no theme matched (READ THESE: they show missing themes and missed phrasings)
Process: 1) draft themes from a first read of the data, 2) run, 3) read the samples and the unmatched list, 4) fix patterns and add
themes, 5) repeat until the samples are about 90% true matches and the unmatched list holds no new theme, 6) only then quote
the percentages. State the final pattern list in the vault note. Counts are keyword-based: say "about" and name the sample read.
Negation is the usual trap ("not worth it" vs "worth it"; "no side effects" vs "side effects"): handle it in the pattern or by hand.
"""
import json, re, sys, os, argparse, collections


def load_amazon(p):
    d = json.load(open(p, encoding='utf-8'))
    rows = []
    if isinstance(d, dict):
        for prod, lst in d.items():
            for r in lst:
                if isinstance(r, dict) and 'b' in r:
                    rows.append((prod, int(r.get('s') or 0), ((r.get('t') or '') + ' ' + r['b']).strip()))
    else:
        for r in d:
            rows.append((r.get('product', ''), int(r.get('stars') or 0), r.get('text', '')))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--themes', required=True)
    ap.add_argument('--amazon')
    ap.add_argument('--reddit')
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    themes = {k: re.compile(v, re.I) for k, v in json.load(open(a.themes, encoding='utf-8')).items()}
    rows = load_amazon(a.amazon) if a.amazon else []
    crit = [r for r in rows if 1 <= r[1] <= 3]
    th = json.load(open(a.reddit, encoding='utf-8')) if a.reddit else []
    comments = [(t['sub'], c[1]) for t in th for c in t.get('comments', []) if isinstance(c, list) and len(c) > 1]
    lines = [f'# Theme counts\n', f'Amazon reviews: {len(rows)} (critical 1-3 star: {len(crit)}). Reddit: {len(th)} threads, {len(comments)} comments.\n',
             '| Theme | All reviews | Critical | % of critical | Reddit threads | Reddit comments |', '|---|---|---|---|---|---|']
    matched_crit = set()
    for name, rx in themes.items():
        allm = [r for r in rows if rx.search(r[2])]
        cm = [r for r in allm if 1 <= r[1] <= 3]
        for r in cm:
            matched_crit.add(id(r))
        tm = [t for t in th if rx.search((t.get('title') or '') + ' ' + (t.get('text') or ''))]
        cmm = [c for c in comments if rx.search(c[1])]
        pct = round(100 * len(cm) / len(crit)) if crit else 0
        lines.append(f'| {name} | {len(allm)} | {len(cm)} | {pct}% | {len(tm)} | {len(cmm)} |')
        per = collections.Counter(r[0] for r in cm)
        with open(os.path.join(a.out, f'samples_{name}.txt'), 'w', encoding='utf-8') as f:
            f.write(f'{name}: pattern = {rx.pattern}\ncritical per product: {dict(per.most_common())}\n\n')
            for r in (cm + [x for x in allm if x not in cm])[:25]:
                f.write(f'[{r[0]} {r[1]}*] {r[2][:400]}\n\n')
            for c in cmm[:8]:
                f.write(f'[reddit {c[0]}] {c[1][:300]}\n\n')
    un = [r for r in crit if id(r) not in matched_crit]
    with open(os.path.join(a.out, 'unmatched_critical.txt'), 'w', encoding='utf-8') as f:
        f.write(f'{len(un)} of {len(crit)} critical reviews matched no theme. Read these for missing themes.\n\n')
        for r in un[:25]:
            f.write(f'[{r[0]} {r[1]}*] {r[2][:400]}\n\n')
    open(os.path.join(a.out, 'theme_counts.md'), 'w', encoding='utf-8').write('\n'.join(lines) + f'\n\nUnmatched critical: {len(un)} of {len(crit)}\n')
    print('\n'.join(lines))
    print(f'unmatched critical: {len(un)} of {len(crit)}')


if __name__ == '__main__':
    main()
