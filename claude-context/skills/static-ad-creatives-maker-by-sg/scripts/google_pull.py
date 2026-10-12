"""Google research for a brand, no DataForSEO (Soumil, 2026-10-09: not buying it now; revisit when a brand needs EXACT search volumes).

Steps:
  autosuggest   free Google suggestions for India (English and Hinglish): what people type, in what order. No volumes. ~500 queries, no key.
  serp          Apify google-search-scraper, one results page per query: People Also Ask, related searches, organic results. $0.0025 per page at Starter.
  trends        Apify google-trends-scraper: one comparison chart of up to 5 terms, 5 years, India. About $0.06 per chart and about 2 minutes
                (set a 290 s timeout; two of three runs timed out at 130 s). Gives month-of-year seasonality, state split, related and rising queries.
  trends_report local read of the trends output: month-of-year table (index 100 = highest weekly point across the terms), latest week, states, related queries.
Reading the numbers: Trends is RELATIVE and sampled; a small term next to a big one shows 0 (too small to register), not zero searches.
Exact monthly counts need DataForSEO (Google Ads volumes, $0.06 per 1,000 keywords, $50 minimum deposit). SERP price there: $0.0006 queued, $0.0012 priority, $0.002 live per page.

Usage:
  python google_pull.py --config C:/cca/<brand>/research/google_config.json --step autosuggest|serp|trends|trends_report [--dry-run]
Config: references/examples/google_config_daigo.json
"""
import os, sys, json, re, time, argparse, collections, datetime, urllib.parse, urllib.request, io

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apify_lib as A  # also sets stdout to UTF-8 (import it once, wrapping stdout twice closes the stream)

DEFAULT_TAGS = {
    'price': r'price|cost|rate|rs\b|\u20b9|kitne|kitna',
    'review': r'review|rating|reviews|genuine|real|fake',
    'health': r'benefit|fayd|protein|gut|probiotic|digest|weight|diabet|side effect|acidity|calorie|nutrition|healthy|sugar',
    'recipe': r'recipe|kaise|how to make|banaye|banane|ghar par|at home|homemade',
    'buy': r'buy|online|near me|amazon|flipkart|blinkit|zepto|instamart|bigbasket|order',
    'season': r'summer|winter|garmi|sardi|monsoon|navratri|vrat|fast|sendha|jain|diwali',
    'travel': r'travel|train|flight|airport|trip|road|hostel|pg|office|hotel',
}


def load_cfg(path):
    cfg = json.load(open(path, encoding='utf-8'))
    cfg['out_dir'] = cfg['out_dir'].rstrip('/\\') + '/'
    os.makedirs(cfg['out_dir'], exist_ok=True)
    return cfg


# ---------- autosuggest (free) ----------
def step_autosuggest(cfg, dry):
    ac = cfg['autosuggest']
    country, lang = ac.get('country', 'in'), ac.get('lang', 'en')
    base = 'https://suggestqueries.google.com/complete/search?client=firefox&hl=%s&gl=%s&q=' % (lang, country)
    queries = []
    for grp, seeds in ac['seeds'].items():
        queries += [(grp, s) for s in seeds]
    for s in ac.get('modifier_seeds', []):
        queries += [('modifier', s + m) for m in ac.get('modifiers', [])]
    for s in ac.get('letter_seeds', []):
        queries += [('letter', s + ' ' + ch) for ch in 'abcdefghijklmnopqrstuvwxyz']
    print('autosuggest queries:', len(queries), '(about %d seconds at 0.5 s each)' % (len(queries) // 2), flush=True)
    if dry:
        return
    out, fails = {}, 0
    for i, (grp, q) in enumerate(queries):
        err = ''
        res = None
        for a in range(3):
            try:
                d = json.load(urllib.request.urlopen(urllib.request.Request(base + urllib.parse.quote(q), headers={'User-Agent': 'Mozilla/5.0'}), timeout=30))
                res = d[1] if isinstance(d, list) and len(d) > 1 else []
                break
            except Exception as e:
                err = str(e)[:80]
                time.sleep(2 * (a + 1))
        if res is None:
            fails += 1
            out[q] = {'group': grp, 'error': err}
            if fails >= 12:
                print('too many failures, stopping at', i, flush=True)
                break
        else:
            out[q] = {'group': grp, 'google': res}
        time.sleep(0.5)
    json.dump(out, open(cfg['out_dir'] + 'autosuggest.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    tags = dict(DEFAULT_TAGS)
    tags.update(ac.get('tags', {}))
    allc = collections.Counter()
    bytag = {t: collections.Counter() for t in tags}
    for q, v in out.items():
        for c in v.get('google', []) or []:
            c = c.strip().lower()
            allc[c] += 1
            for t, pat in tags.items():
                if re.search(pat, c):
                    bytag[t][c] += 1
    lines = ['# Google autosuggest, %s' % datetime.date.today().isoformat(), '', 'Completions only: they show what people type, not how often. Queries sent: %d, failures: %d, distinct completions: %d.' % (len(queries), fails, len(allc)), '',
             '| Type | Distinct completions |', '|---|---|']
    lines += ['| %s | %d |' % (t, len(bytag[t])) for t in tags]
    for t in tags:
        lines += ['', '## Top completions: %s' % t, ''] + ['- %s (%d)' % (c, n) for c, n in bytag[t].most_common(30)]
    lines += ['', '## First 6 completions per core seed', '']
    for q, v in out.items():
        if v.get('group') in ac['seeds']:
            lines.append('- [%s] %s: %s' % (v['group'], q, ' | '.join((v.get('google') or [])[:6]) if v.get('google') else v.get('error', '')))
    open(cfg['out_dir'] + 'autosuggest_summary.md', 'w', encoding='utf-8').write('\n'.join(lines))
    print('written; fails', fails, 'distinct', len(allc), flush=True)


# ---------- Apify: serp + trends ----------
def step_serp(cfg, dry):
    sc = cfg['serp']
    qs = sc['queries']
    print('serp: %d queries, one page each, about $%.2f' % (len(qs), len(qs) * 0.0025), flush=True)
    if dry:
        return
    inp = {'queries': '\n'.join(qs), 'maxPagesPerQuery': 1, 'countryCode': sc.get('country_code', 'in'), 'languageCode': sc.get('language_code', 'en'), 'mobileResults': False, 'saveHtmlToKeyValueStore': False}
    # the actor refuses a per-run cap below $0.50 (real cost is about $0.0025 per page), so the cap is a ceiling, not the expected spend
    r = A.run_and_collect('serp', 'apify~google-search-scraper', inp, max(0.5, float(sc.get('cap', '0.50'))), max_wait=500, timeout_secs=500)
    json.dump(r['items'], open(cfg['out_dir'] + 'apify_serp.json', 'w', encoding='utf-8'), ensure_ascii=False)
    paa = sum(len(it.get('peopleAlsoAsk') or []) for it in r['items'])
    print('serp: status=%s pages=%d, People Also Ask questions %d, secs=%s err=%s' % (r.get('status'), len(r['items']), paa, r['secs'], r.get('err')), flush=True)


def step_trends(cfg, dry):
    import threading
    tc = cfg['trends']
    charts = tc['compare']
    print('trends: %d comparison chart(s), about $%.2f and 2+ minutes each' % (len(charts), 0.07 * len(charts)), flush=True)
    if dry:
        return
    res = {}

    def go(i, terms):
        inp = {'searchTerms': [terms], 'isMultiple': True, 'timeRange': tc.get('time_range', 'today 5-y'), 'geo': tc.get('geo', 'IN'), 'viewedFrom': tc.get('geo', 'IN').lower(), 'skipDebugScreen': True}
        res[i] = A.run_and_collect('trends_%d' % i, 'apify~google-trends-scraper', inp, tc.get('cap', '0.30'), max_wait=300, timeout_secs=290)

    ths = [threading.Thread(target=go, args=(i, t)) for i, t in enumerate(charts)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    for i, r in res.items():
        json.dump(r['items'], open(cfg['out_dir'] + 'apify_trends_%d.json' % i, 'w', encoding='utf-8'), ensure_ascii=False)
        print('trends %d: status=%s items=%d secs=%s err=%s' % (i, r.get('status'), len(r['items']), r['secs'], r.get('err')), flush=True)


def step_trends_report(cfg, dry):
    import glob
    MN = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    for fn in sorted(glob.glob(cfg['out_dir'] + 'apify_trends_*.json')) + sorted(glob.glob(cfg['out_dir'] + 'apify_test_trends_*.json')):
        items = json.load(open(fn, encoding='utf-8'))
        if not items:
            continue
        it = items[0]
        terms = [t.strip() for t in (it.get('searchTerm') or '').split(',')]
        tl = it.get('interestOverTime_timelineData') or []
        print('\n=== %s | terms: %s | weekly points %d' % (os.path.basename(fn), terms, len(tl)))
        prof = collections.defaultdict(lambda: collections.defaultdict(list))
        for p in tl:
            try:
                dt = datetime.datetime.fromtimestamp(int(p.get('time')), datetime.timezone.utc)
            except Exception:
                continue
            for i, v in enumerate(p.get('value') or []):
                if i < len(terms):
                    try:
                        prof[terms[i]][dt.month].append(float(v))
                    except Exception:
                        pass
        print('month-of-year average index (100 = highest weekly point across the terms)')
        print('term'.ljust(18) + ' '.join(m.rjust(4) for m in MN))
        for t in terms:
            row = [('%d' % round(sum(prof[t][m]) / len(prof[t][m]))) if prof[t].get(m) else '-' for m in range(1, 13)]
            print(t[:17].ljust(18) + ' '.join(r.rjust(4) for r in row))
        if tl:
            print('latest week:', tl[-1].get('formattedTime'), dict(zip(terms, tl[-1].get('formattedValue') or [])))
        print('top related:', [(q.get('query'), q.get('value')) for q in (it.get('relatedQueries_top') or [])[:6]])
        print('rising related:', [(q.get('query'), q.get('formattedValue')) for q in (it.get('relatedQueries_rising') or [])[:6]])
        sub = it.get('interestBySubregion') or []
        if sub and len(terms) >= 2:
            for ti in range(min(2, len(terms))):
                top = sorted(sub, key=lambda s: -(s.get('value') or [0] * 5)[ti] if len(s.get('value') or []) > ti else 0)[:8]
                print('states where "%s" has the biggest share of these terms:' % terms[ti], [(s.get('geoName'), (s.get('value') or [0])[ti]) for s in top])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--step', required=True, choices=['autosuggest', 'serp', 'trends', 'trends_report'])
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    {'autosuggest': step_autosuggest, 'serp': step_serp, 'trends': step_trends, 'trends_report': step_trends_report}[a.step](cfg, a.dry_run)
