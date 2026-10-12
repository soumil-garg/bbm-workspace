"""Amazon.in reviews through Apify, no login, no Chrome (proven on Daigo, 2026-10-09: 748+ reviews from 67 listings for about $2, 56% critical).

What each actor gives (verified 2026-10-09 on amazon.in):
  jaybird~amazon-reviews-scraper   a summary row per listing (average, rating count, STAR HISTOGRAM IN PERCENT) plus the product page's top reviews
                                   (about 4 per listing on average, up to about 13). $0.00092 per item at Starter. Good for breadth.
  axesso_data~amazon-reviews-scraper  review pages with sortBy, maxPages (3 used) and filterByStar. Gets past the 13-review wall: 55 unique reviews
                                   from one listing (21 of them 1-star). $0.0009 per review. Used for the critical (1 to 3 star) reviews and small listings.
Many ratings are star-only (no text), so the review count held is lower than the rating count shown.
Dead ends: jdtpnjtp/amazon-reviews has no India; DataForSEO's Amazon reviews endpoint is documented as down; Chrome with a logged-in profile is the old
fallback (research-playbook section 2) and risks the account (Amazon limits flagged accounts to 8 reviews).
Ask Soumil for a yes before the first Amazon pull of a brand (public pages, none of his logins used).

Usage:
  python amazon_pull.py --config C:/cca/<brand>/research/amazon_config.json --step depth|public|deep|ext|compile|all [--dry-run]
Config: references/examples/amazon_config_daigo.json. The ASIN csv has columns asin,title,brand,group,url,rating,ratings_count,source
(the competitor research agent writes it from amazon.in-restricted searches).
"""
import os, sys, json, csv, re, math, argparse, collections, glob, datetime, threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apify_lib as A

ACT_PUBLIC = 'jaybird~amazon-reviews-scraper'
ACT_DEEP = 'axesso_data~amazon-reviews-scraper'
DEFAULTS = {'domain': 'amazon.in', 'domain_code': 'in', 'depth_test_asin': '', 'depth_pass_min_unique': 25, 'big_min_ratings': 100, 'deep_top_n': 8, 'ext_min_ratings': 8,
            'force_asins': [], 'group_priority': {}, 'key_asins': [], 'max_reviews_per_asin': 30, 'price_review': 0.0009,
            'caps': {'depth': '0.25', 'public_chunk': '0.70', 'deep': '0.90', 'ext_chunk': '0.65'}}
lock = threading.Lock()
LOGF = [None]


def log(msg):
    line = '%s %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)
    with lock:
        print(line, flush=True)
        if LOGF[0]:
            with open(LOGF[0], 'a', encoding='utf-8') as f:
                f.write(line + '\n')


def load_cfg(path):
    cfg = json.load(open(path, encoding='utf-8'))
    out = json.loads(json.dumps(DEFAULTS))
    for k, v in cfg.items():
        if k == 'caps':
            out['caps'].update(v)
        else:
            out[k] = v
    out['out_dir'] = out['out_dir'].rstrip('/\\') + '/'
    os.makedirs(out['out_dir'], exist_ok=True)
    return out


def read_rows(cfg):
    return list(csv.DictReader(open(cfg['asin_csv'], encoding='utf-8')))


def rc(r):
    try:
        return int(str(r['ratings_count']).replace(',', '') or 0)
    except Exception:
        return 0


def valid_asins(rows):
    out = []
    for r in rows:
        a = (r.get('asin') or '').strip()
        if re.fullmatch(r'[A-Z0-9]{10}', a) and a not in out:
            out.append(a)
    return out


def num(v):
    m = re.search(r'(\d+(?:\.\d+)?)', str(v or ''))
    return float(m.group(1)) if m else None


def state_path(cfg):
    return cfg['out_dir'] + 'state.json'


def get_state(cfg):
    p = state_path(cfg)
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}


def put_state(cfg, **kw):
    s = get_state(cfg)
    s.update(kw)
    json.dump(s, open(state_path(cfg), 'w', encoding='utf-8'), indent=1)


# ---------- steps ----------
def step_depth(cfg, dry):
    a = cfg['depth_test_asin']
    if not a:
        log('depth: no depth_test_asin in the config (pick the listing with the most ratings)')
        return
    dc = cfg['domain_code']
    inp = {'input': [{'asin': a, 'domainCode': dc, 'sortBy': 'recent', 'maxPages': 3, 'filterByStar': 'one_star'},
                     {'asin': a, 'domainCode': dc, 'sortBy': 'helpful', 'maxPages': 3},
                     {'asin': a, 'domainCode': dc, 'sortBy': 'recent', 'maxPages': 3, 'filterByStar': 'two_star'}]}
    log('depth test on %s: up to 90 reviews, about $0.08' % a)
    if dry:
        return
    r = A.run_and_collect('depth_test', ACT_DEEP, inp, cfg['caps']['depth'], max_wait=400, timeout_secs=400)
    items = r['items']
    json.dump(items, open(cfg['out_dir'] + 'depth_test_axesso.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    uniq = {it.get('reviewId') for it in items if it.get('reviewId') and not str(it.get('statusMessage')).startswith('NO_REVIEWS')}
    ok = len(uniq) >= cfg['depth_pass_min_unique']
    log('depth test: status=%s items=%d unique reviews=%d -> %s' % (r.get('status'), len(items), len(uniq), 'PASSED, deep pulls allowed' if ok else 'FAILED, public layer only'))
    put_state(cfg, depth_unique=len(uniq), deep_ok=ok)


def step_public(cfg, dry):
    asins = valid_asins(read_rows(cfg))
    chunks = [asins[i::3] for i in range(3)]
    log('public layer: %d ASINs in 3 runs, expected about %d items, about $%.2f' % (len(asins), len(asins) * 4.5, len(asins) * 4.5 * 0.00092))
    if dry:
        return
    res = {}

    def jb(k, chunk):
        inp = {'asins': chunk, 'domain': cfg['domain'], 'maxReviewsPerAsin': cfg['max_reviews_per_asin'], 'includeMediaReviews': False}
        res[k] = A.run_and_collect('jaybird_%d' % k, ACT_PUBLIC, inp, cfg['caps']['public_chunk'], max_wait=1500, timeout_secs=1500)
        log('public chunk %d: status=%s items=%d secs=%s err=%s' % (k, res[k].get('status'), len(res[k]['items']), res[k]['secs'], res[k].get('err')))

    ths = [threading.Thread(target=jb, args=(k, c)) for k, c in enumerate(chunks)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    allj = []
    for k in sorted(res):
        allj.extend(res[k]['items'])
    json.dump(allj, open(cfg['out_dir'] + 'jaybird_public_layer.json', 'w', encoding='utf-8'), ensure_ascii=False)
    log('public layer total items %d' % len(allj))


def step_deep(cfg, dry):
    st = get_state(cfg)
    if not st.get('deep_ok'):
        log('deep: the depth test has not passed (run --step depth first); skipping')
        return
    rows = read_rows(cfg)
    big = [r['asin'] for r in sorted(rows, key=rc, reverse=True) if rc(r) >= cfg['big_min_ratings']][:cfg['deep_top_n']]
    inp = {'input': []}
    for a in big:
        for star in ['one_star', 'two_star', 'three_star']:
            inp['input'].append({'asin': a, 'domainCode': cfg['domain_code'], 'sortBy': 'recent', 'maxPages': 3, 'filterByStar': star})
    log('deep critical pull: %d listings x 3 star filters, up to %d reviews, about $%.2f' % (len(big), len(inp['input']) * 30, len(inp['input']) * 30 * cfg['price_review']))
    if dry:
        return
    r = A.run_and_collect('axesso_deep', ACT_DEEP, inp, cfg['caps']['deep'], max_wait=1500, timeout_secs=1500)
    json.dump(r['items'], open(cfg['out_dir'] + 'axesso_deep_critical.json', 'w', encoding='utf-8'), ensure_ascii=False)
    put_state(cfg, deep_asins=big)
    log('deep pull: status=%s items=%d secs=%s err=%s' % (r.get('status'), len(r['items']), r['secs'], r.get('err')))


def compile_all(cfg, plan=True):
    rows = read_rows(cfg)
    meta = {r['asin']: r for r in rows}
    out = cfg['out_dir']
    reviews, summ = {}, {}

    def add(asin, rid, rating, title, text, date, verified, helpful, src):
        if not rid:
            return
        key = (asin, rid)
        if key in reviews:
            reviews[key]['srcs'].add(src)
            return
        reviews[key] = {'asin': asin, 'review_id': rid, 'rating': rating, 'title': title or '', 'text': text or '', 'date': date or '', 'verified': verified, 'helpful': helpful, 'srcs': {src}}

    p = out + 'jaybird_public_layer.json'
    if os.path.exists(p):
        for it in json.load(open(p, encoding='utf-8')):
            a = it.get('asin')
            if it.get('recordType') == 'summary':
                summ[a] = {'avg': it.get('averageRating'), 'count': it.get('totalRatingCount'), 'hist_pct': it.get('ratingsHistogram'), 'title': it.get('productTitle'), 'customers_say': it.get('customersSay')}
            elif it.get('recordType') == 'review':
                add(a, it.get('reviewId'), num(it.get('rating')), it.get('title'), it.get('text'), it.get('date'), it.get('verifiedPurchase'), it.get('helpfulVotes'), 'jaybird')
    n_jb = len(reviews)
    files = ['depth_test_axesso.json', 'axesso_deep_critical.json'] + sorted(os.path.basename(x) for x in glob.glob(out + 'axesso_ext_*.json'))
    for fn in files:
        if not os.path.exists(out + fn):
            continue
        for it in json.load(open(out + fn, encoding='utf-8')):
            if str(it.get('statusMessage')).startswith('NO_REVIEWS'):
                continue
            add(it.get('asin'), it.get('reviewId'), num(it.get('rating')), it.get('title'), it.get('text'), it.get('date'), it.get('verified'), it.get('numberOfHelpful'), 'axesso')
    allr = list(reviews.values())
    for r in allr:
        r['srcs'] = sorted(r['srcs'])
        r['group'] = (meta.get(r['asin']) or {}).get('group', '?')
        r['brand'] = (meta.get(r['asin']) or {}).get('brand', '?')
    json.dump(allr, open(out + 'amazon_reviews_all.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(summ, open(out + 'amazon_summaries.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    crit = [r for r in allr if r['rating'] is not None and r['rating'] <= 3]
    log('unique reviews %d (public layer %d, added by axesso %d) | listings with a summary %d | listings with a review %d' % (len(allr), n_jb, len(allr) - n_jb, len(summ), len({r['asin'] for r in allr})))
    log('critical (1 to 3 star): %d of %d = %.0f%% | with text of 20+ characters: %d' % (len(crit), len(allr), 100.0 * len(crit) / max(1, len(allr)), sum(1 for r in allr if len((r['text'] or '').strip()) >= 20)))
    log('rating mix: %s' % dict(sorted(collections.Counter(int(r['rating']) if r['rating'] else 0 for r in allr).items())))
    byg = collections.defaultdict(list)
    for r in allr:
        byg[r['group']].append(r)
    for g, lst in sorted(byg.items(), key=lambda x: -len(x[1])):
        log('  group %-22s reviews %4d | critical %4d | listings %2d' % (g, len(lst), sum(1 for r in lst if r['rating'] and r['rating'] <= 3), len({r['asin'] for r in lst})))
    cnt = collections.Counter(r['asin'] for r in allr)
    for a in cfg['key_asins']:
        s = summ.get(a) or {}
        h = s.get('hist_pct') or {}
        log('  key %s %-10s histogram %% 5/4/3/2/1 = %s/%s/%s/%s/%s | avg %s of %s ratings | reviews held %d' % (a, (meta.get(a) or {}).get('brand', '?')[:10], h.get('fiveStar'), h.get('fourStar'), h.get('threeStar'), h.get('twoStar'), h.get('oneStar'), s.get('avg'), s.get('count'), cnt.get(a, 0)))
    if not plan:
        return summ, cnt
    st_ = get_state(cfg)
    deep_done = set(st_.get('deep_asins', [])) | set(st_.get('ext_asins', []))
    plan_rows = []
    for a, s in summ.items():
        c = s.get('count') or 0
        held = cnt.get(a, 0)
        if a in deep_done or c < cfg['ext_min_ratings'] or c <= held + 2:
            continue
        g = (meta.get(a) or {}).get('group', '?')
        plan_rows.append({'asin': a, 'group': g, 'count': c, 'held': held, 'prio': cfg['group_priority'].get(g, 5)})
    plan_rows.sort(key=lambda x: (x['prio'], -x['count']))
    entries, est = [], 0
    for p_ in plan_rows:
        if p_['count'] < 60:
            pages = min(6, max(1, math.ceil(p_['count'] / 10.0)))
            entries.append({'asin': p_['asin'], 'domainCode': cfg['domain_code'], 'sortBy': 'recent', 'maxPages': pages})
            est += min(p_['count'], pages * 10)
        else:
            for star in ['one_star', 'two_star', 'three_star']:
                entries.append({'asin': p_['asin'], 'domainCode': cfg['domain_code'], 'sortBy': 'recent', 'maxPages': 3, 'filterByStar': star})
            est += 45
    have = {e['asin'] for e in entries}
    for a in cfg['force_asins']:
        if a not in have:
            entries.append({'asin': a, 'domainCode': cfg['domain_code'], 'sortBy': 'recent', 'maxPages': 4})
    json.dump({'plan': plan_rows, 'entries': entries, 'est_items': est}, open(out + 'ext_plan.json', 'w', encoding='utf-8'), indent=1)
    log('extension plan: %d listings, %d entries, about %d reviews, about $%.2f' % (len(plan_rows), len(entries), est, est * cfg['price_review']))
    return summ, cnt


def step_ext(cfg, dry):
    compile_all(cfg)
    entries = json.load(open(cfg['out_dir'] + 'ext_plan.json', encoding='utf-8'))['entries']
    if dry or not entries:
        return
    chunks = [entries[i::3] for i in range(3)]
    res = {}

    def go(k, chunk):
        r = A.run_and_collect('axesso_ext_%d' % k, ACT_DEEP, {'input': chunk}, cfg['caps']['ext_chunk'], max_wait=1500, timeout_secs=1500)
        res[k] = r
        with open(cfg['out_dir'] + 'axesso_ext_%d.json' % k, 'w', encoding='utf-8') as f:
            json.dump(r['items'], f, ensure_ascii=False)
        log('ext chunk %d: entries=%d status=%s items=%d secs=%s err=%s' % (k, len(chunk), r.get('status'), len(r['items']), r['secs'], r.get('err')))

    ths = [threading.Thread(target=go, args=(k, c)) for k, c in enumerate(chunks)]
    [t.start() for t in ths]
    [t.join() for t in ths]
    put_state(cfg, ext_asins=sorted({e['asin'] for e in entries}))   # so a re-run does not pay twice for star-only ratings
    compile_all(cfg, plan=False)


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--step', required=True, choices=['depth', 'public', 'deep', 'ext', 'compile', 'all'])
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    LOGF[0] = None if a.dry_run else cfg['out_dir'] + 'amazon_log.txt'
    steps = {'depth': step_depth, 'public': step_public, 'deep': step_deep, 'ext': step_ext, 'compile': lambda c, d: compile_all(c)}
    if a.step == 'all':
        for name in ['depth', 'public', 'deep', 'compile', 'ext']:
            log('--- step %s' % name)
            steps[name](cfg, a.dry_run)
        if not a.dry_run:
            used, limit = A.month_usage()
            log('account monthly usage now %s of limit %s (billing can lag a minute)' % (used, limit))
    else:
        steps[a.step](cfg, a.dry_run)
