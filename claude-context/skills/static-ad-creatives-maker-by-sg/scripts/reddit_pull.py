"""Reddit research through Apify, config driven (proven on Daigo, 2026-10-09: 3,416 threads and 8,037 comments for about $7).

Why Apify: Reddit blocks WebFetch, curl and Chrome, and the free archives (Arctic Shift, PullPush) time out or return 429 for hours.
Two phases, because comments are where the customer voice is and they are cheaper than posts per item:
  phase 1    find posts (no comments) from date_from to date_to with strict matching, plus comment-level brand mentions
  phase 2    pull comments only for the relevant threads, fitted to a budget by lowering the caps step by step
  topup      older windows (the newest-first caps in phase 1 cut older years): posts, then comments
Every run is started with a per-run cap; spend is estimated as items x list price; the account limit is never raised by this script.
Public text only. Ask Soumil for a yes before the first Reddit pull of a brand (terms-adverse, public data, none of his logins used).

Usage:
  python reddit_pull.py --config C:/cca/<brand>/research/reddit_config.json --phase 1 [--dry-run]
  python reddit_pull.py --config ... --phase 2 [--dry-run]
  python reddit_pull.py --config ... --phase topup [--dry-run]
Config: see references/examples/reddit_config_daigo.json (words, query_groups, sub_jobs, use_case_*, mention_terms, schedule, budgets).
Word lists are regex fragments wrapped in word boundaries (so 'lassi' does not match 'classic'). 'indic' words count in any subreddit;
'english' words (e.g. buttermilk) count only in India-related subreddits, to keep out US baking threads.
"""
import os, sys, json, re, argparse, threading, datetime, collections
import concurrent.futures as cf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import apify_lib as A

ACT_POSTS = 'fatihtahta~reddit-scraper-search-fast'      # $0.00139 per item at Starter (posts and comments alike)
ACT_COMMENTS = 'automation-lab~reddit-scraper'            # start $0.003, post $0.001, comment $0.0005 at Starter (slower, cheapest for comments)
ACT_MENTIONS = 'harshmaur~reddit-scraper'                 # comment keyword search: $0.0018 per result + $0.02 start

DEFAULTS = {
    'date_from': '2023-10-09', 'date_to': '2026-10-09',
    'budget_posts': 4.5, 'budget_comments': 4.8, 'budget_topup_posts': 1.0, 'budget_topup_comments': 1.2,
    'chunk': 15, 'workers_posts': 6, 'workers_comments': 8,
    'price_post_item': 0.00139, 'price_mention_init': 0.02, 'price_mention_item': 0.0018,
    'price_comment_start': 0.003, 'price_comment_post': 0.001, 'price_comment_comment': 0.0005,
    'words': {'indic': [], 'english': [], 'india_hints': ['india', 'indian', 'desi', 'mumbai', 'delhi', 'pune', 'bangalore', 'bengaluru', 'hyderabad', 'chennai', 'kolkata',
                                                         'gurgaon', 'gurugram', 'noida', 'ahmedabad', 'nagpur', 'surat', 'jaipur', 'lucknow', 'kerala', 'tamil', 'gujarat',
                                                         'punjab', 'bihar', 'maharashtra', 'indic', 'bharat', 'bakchod'],
              'india_exact': ['jeeneetards', 'btechtards', 'catpreparation', 'twentiesindia', 'indianteenagers', 'fitness_india', 'snacksindia', 'aajmainekhaya']},
    'query_groups': [], 'sub_jobs': [], 'use_case_subs': [], 'use_case_groups': {}, 'use_case_max_posts': 40, 'use_case_cap': '0.25',
    'global_use_case_queries': [], 'global_use_case_max_posts': 40,
    'mention_terms': [], 'mention_max_comments': 100, 'mention_cap': '1.60',
    'use_regex': '', 'brand_regex': '', 'use_min_comments': 30, 'brand_min_comments': 15,
    'schedule': [[80, 40, 40, 30, 2, 5], [80, 30, 30, 30, 2, 8], [60, 30, 30, 25, 3, 8], [60, 25, 25, 20, 3, 10], [50, 20, 25, 20, 4, 10], [40, 20, 20, 15, 4, 10],
                 [30, 15, 20, 15, 5, 10], [25, 15, 15, 10, 5, 15]],
    'topup_windows': [], 'topup_subs': [], 'topup_sub_keywords': [], 'topup_schedule': [[60, 30, 2, 5], [50, 25, 3, 8], [40, 20, 4, 10], [30, 15, 5, 12], [20, 10, 6, 15]],
}


def load_cfg(path):
    cfg = json.load(open(path, encoding='utf-8'))
    out = json.loads(json.dumps(DEFAULTS))
    for k, v in cfg.items():
        if k == 'words' and isinstance(v, dict):
            out['words'].update(v)
        else:
            out[k] = v
    if not out.get('out_dir'):
        raise SystemExit('config needs out_dir')
    out['out_dir'] = out['out_dir'].rstrip('/\\') + '/'
    os.makedirs(out['out_dir'], exist_ok=True)
    return out


lock = threading.Lock()
LOGF = [None]


def log(msg):
    line = '%s %s' % (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)
    with lock:
        print(line, flush=True)
        if LOGF[0]:
            with open(LOGF[0], 'a', encoding='utf-8') as f:
                f.write(line + '\n')


def words_rx(words):
    return re.compile('|'.join(r'\b' + w + r'\b' for w in words), re.I) if words else None


class Rel:
    def __init__(self, cfg):
        w = cfg['words']
        self.indic = words_rx(w['indic'])
        self.eng = words_rx(w['english'])
        self.hints = [h.lower() for h in w['india_hints']]
        self.exact = {e.lower() for e in w['india_exact']}
        self.use = re.compile(cfg['use_regex'], re.I) if cfg['use_regex'] else None
        self.brand = re.compile(cfg['brand_regex'], re.I) if cfg['brand_regex'] else None
        both = [x for x in (w['indic'] + w['english'])]
        self.any = words_rx(both)

    def is_india(self, sub):
        s = (sub or '').lower()
        return s in self.exact or any(h in s for h in self.hints)

    def tier(self, p):
        title, body = p.get('title') or '', p.get('body') or ''
        ind = self.is_india(p.get('subreddit'))
        nc = ncom(p)
        if (self.indic and self.indic.search(title)) or (self.eng and self.eng.search(title) and ind):
            return 'T1'
        if ((self.indic and self.indic.search(body)) or (self.eng and self.eng.search(body))) and ind:
            return 'T2'
        return None


def ncom(p):
    try:
        return int(p.get('num_comments') or 0)
    except Exception:
        return 0


# ---------- job builders ----------
def base_posts(cfg, d0=None, d1=None):
    return {'sort': 'new', 'timeframe': 'all', 'dateFrom': d0 or cfg['date_from'], 'dateTo': d1 or cfg['date_to'], 'forceSortNewForTimeFilteredRuns': True,
            'scrapeComments': False, 'strictSearch': True, 'strictTokenFilter': True}


def qjob(cfg, tag, queries, maxposts, cap, d0=None, d1=None):
    inp = base_posts(cfg, d0, d1)
    inp.update({'queries': queries, 'maxPosts': maxposts})
    return {'tag': tag, 'actor': ACT_POSTS, 'inp': inp, 'cap': cap, 'kind': 'A', 'what': queries}


def sjob(cfg, tag, sub, kws, maxposts, cap, d0=None, d1=None):
    inp = base_posts(cfg, d0, d1)
    inp.update({'subredditName': sub, 'subredditKeywords': kws, 'subredditSort': 'new', 'subredditTimeframe': 'all', 'maxPosts': maxposts})
    return {'tag': tag, 'actor': ACT_POSTS, 'inp': inp, 'cap': cap, 'kind': 'A', 'what': [sub] + kws}


def cjob(cfg, tag, terms, maxc, cap):
    inp = {'searchTerms': terms, 'searchPosts': False, 'searchComments': True, 'searchSort': 'new', 'searchTime': 'all', 'commentedAfter': cfg['date_from'], 'maxCommentsCount': maxc}
    return {'tag': tag, 'actor': ACT_MENTIONS, 'inp': inp, 'cap': cap, 'kind': 'C', 'what': terms}


def phase1_jobs(cfg):
    jobs = []
    for g in cfg['query_groups']:
        jobs.append(qjob(cfg, g['tag'], g['queries'], g.get('max_posts', 100), g.get('cap', '0.50')))
    for sj in cfg['sub_jobs']:
        for sub in sj['subs']:
            jobs.append(sjob(cfg, '%s_%s' % (sj['tag_prefix'], sub), sub, sj['keywords'], sj.get('max_posts', 60), sj.get('cap', '0.15')))
    for sub in cfg['use_case_subs']:
        for g, kws in cfg['use_case_groups'].items():
            jobs.append(sjob(cfg, '%s_%s' % (g, sub), sub, kws, cfg['use_case_max_posts'], cfg['use_case_cap']))
    gq = cfg['global_use_case_queries']
    for i in range(0, len(gq), 10):
        jobs.append(qjob(cfg, 'q3%s_use_cases' % 'abcdefgh'[i // 10], gq[i:i + 10], cfg['global_use_case_max_posts'], '0.50'))
    if cfg['mention_terms']:
        jobs.append(cjob(cfg, 'c_mentions', cfg['mention_terms'], cfg['mention_max_comments'], cfg['mention_cap']))
    return jobs


# ---------- phase 1 ----------
def phase1(cfg, dry):
    rel = Rel(cfg)
    jobs = phase1_jobs(cfg)
    log('=== phase 1: %d jobs, posts budget $%.2f, window %s to %s' % (len(jobs), cfg['budget_posts'], cfg['date_from'], cfg['date_to']))
    if dry:
        for j in jobs:
            log('DRY %-34s %s cap $%s  %s' % (j['tag'], j['kind'], j['cap'], ', '.join(j['what'][:6])))
        log('DRY: sum of per-run caps $%.2f (worst case), budget guard stops new jobs at $%.2f of estimated spend' % (sum(float(j['cap']) for j in jobs), cfg['budget_posts']))
        return
    state = {'est': 0.0}
    res = {}

    def run_job(job):
        if state['est'] >= cfg['budget_posts']:
            res[job['tag']] = {'skipped': 'budget'}
            log('SKIP %s: estimated spend %.2f reached budget' % (job['tag'], state['est']))
            return
        r = A.run_and_collect(job['tag'], job['actor'], job['inp'], job['cap'], max_wait=900, timeout_secs=900)
        items = r['items']
        est = (cfg['price_mention_init'] + len(items) * cfg['price_mention_item']) if job['kind'] == 'C' else len(items) * cfg['price_post_item']
        with lock:
            state['est'] += est
        nrel = sum(1 for it in items if rel.any and rel.any.search((it.get('title') or '') + ' ' + (it.get('body') or '')))
        with open(cfg['out_dir'] + 'p1_' + job['tag'] + '.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False)
        res[job['tag']] = {'status': r.get('status'), 'items': len(items), 'rel': nrel, 'est_cost': round(est, 4), 'secs': r['secs'], 'err': r.get('err'), 'run_id': r.get('run_id')}
        log('DONE %-30s status=%s items=%-5d rel=%-5d est$%.3f total_est$%.2f %s' % (job['tag'], r.get('status'), len(items), nrel, est, state['est'], r.get('err') or ''))

    first = next((j for j in jobs if j['kind'] == 'A' and 'subredditName' in j['inp']), jobs[0])
    rest = [j for j in jobs if j is not first]
    run_job(first)
    fr = res.get(first['tag']) or {}
    if fr.get('status') != 'SUCCEEDED':
        log('ABORT: first job did not succeed: %s' % json.dumps(fr))
        return
    if fr['items'] >= 10 and fr['rel'] < 0.4 * fr['items']:
        log('ABORT: first job returned mostly irrelevant posts (%d of %d). Keyword narrowing is not working; fix the config.' % (fr['rel'], fr['items']))
        return
    log('first job ok: items=%d rel=%d' % (fr['items'], fr['rel']))
    with cf.ThreadPoolExecutor(max_workers=cfg['workers_posts']) as ex:
        for f in [ex.submit(run_job, j) for j in rest]:
            try:
                f.result()
            except Exception as e:
                log('JOB EXCEPTION %r' % e)
    posts, mentions = {}, []
    for tag in res:
        p = cfg['out_dir'] + 'p1_' + tag + '.json'
        if not os.path.exists(p):
            continue
        for it in json.load(open(p, encoding='utf-8')):
            if tag == 'c_mentions':
                mentions.append(it)
            elif it.get('kind') == 'post' and it.get('id'):
                if it['id'] not in posts:
                    it['_src'] = tag
                    posts[it['id']] = it
    json.dump(list(posts.values()), open(cfg['out_dir'] + 'p1_posts_all.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(mentions, open(cfg['out_dir'] + 'p1_comment_mentions.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(res, open(cfg['out_dir'] + 'p1_results.json', 'w', encoding='utf-8'), indent=1)
    log('=== phase 1 done: unique posts %d, comment mentions %d, estimated spend $%.2f' % (len(posts), len(mentions), state['est']))
    used, limit = A.month_usage()
    log('account monthly usage now %s of limit %s (billing can lag a minute)' % (used, limit))


# ---------- selection + phase 2 ----------
def select_threads(cfg, rel, posts, label=''):
    T1, T2, T3 = [], [], []
    for p in posts:
        t = rel.tier(p)
        if t == 'T1':
            T1.append(p)
        elif t == 'T2':
            T2.append(p)
        elif rel.is_india(p.get('subreddit')):
            title = p.get('title') or ''
            if (rel.use and rel.use.search(title) and ncom(p) >= cfg['use_min_comments']) or (rel.brand and rel.brand.search(title) and ncom(p) >= cfg['brand_min_comments']):
                T3.append(p)
    for L in (T1, T2, T3):
        L.sort(key=lambda p: -ncom(p))
    log('%stiers: T1 title-match %d, T2 body-match in India subs %d, T3 use-case/brand %d' % (label, len(T1), len(T2), len(T3)))
    return T1, T2, T3


def fit_plan(cfg, T1, T2, T3, budget, schedule, use_t3=True):
    chunk = cfg['chunk']
    for params in schedule:
        if use_t3:
            c1, c2, c3, n3, m1, m2 = params
        else:
            c1, c2, m1, m2 = params
            c3, n3 = 0, 0
        sel = [(p, min(ncom(p), c1), 'T1', c1) for p in T1 if ncom(p) >= m1] + [(p, min(ncom(p), c2), 'T2', c2) for p in T2 if ncom(p) >= m2]
        sel += [(p, min(ncom(p), c3), 'T3', c3) for p in T3[:n3]]
        g = collections.defaultdict(list)
        for s in sel:
            g[s[3]].append(s)
        runs = sum((len(v) + chunk - 1) // chunk for v in g.values())
        est = sum(cfg['price_comment_post'] + s[1] * cfg['price_comment_comment'] for s in sel) + runs * cfg['price_comment_start']
        log('plan %s -> threads %d, runs %d, est $%.2f' % (str(params), len(sel), runs, est))
        if est <= budget:
            return params, sel, est, runs
    return None


def comment_jobs(cfg, sel, prefix):
    byg = collections.defaultdict(list)
    for s in sel:
        byg[s[3]].append(s)
    jobs, k = [], 0
    for cap, lst in byg.items():
        for i in range(0, len(lst), cfg['chunk']):
            part = lst[i:i + cfg['chunk']]
            k += 1
            want = sum(x[1] for x in part)
            ce = cfg['price_comment_start'] + len(part) * cfg['price_comment_post'] + want * cfg['price_comment_comment']
            jobs.append({'tag': '%s%02d_cap%d' % (prefix, k, cap), 'inp': {'urls': [x[0].get('url') for x in part], 'includeComments': True, 'maxCommentsPerPost': cap,
                                                                           'commentDepth': 3, 'deduplicatePosts': True},
                         'cap_usd': '%.2f' % (ce * 1.35 + 0.05), 'est': ce, 'want': want, 'n': len(part)})
    return jobs


def run_comment_jobs(cfg, jobs, file_prefix, label):
    state = {'est': 0.0}
    res = {}

    def run_job(j):
        r = A.run_and_collect(j['tag'], ACT_COMMENTS, j['inp'], j['cap_usd'], max_wait=1500, timeout_secs=1500)
        items = r['items']
        ncm = sum(1 for it in items if it.get('type') == 'comment')
        npo = sum(1 for it in items if it.get('type') == 'post')
        e = cfg['price_comment_start'] + npo * cfg['price_comment_post'] + ncm * cfg['price_comment_comment']
        with lock:
            state['est'] += e
        with open(cfg['out_dir'] + file_prefix + j['tag'] + '.json', 'w', encoding='utf-8') as f:
            json.dump(items, f, ensure_ascii=False)
        res[j['tag']] = {'status': r.get('status'), 'posts': npo, 'comments': ncm, 'want': j['want'], 'est': round(e, 4), 'secs': r['secs'], 'err': r.get('err'), 'run_id': r.get('run_id')}
        log('%sDONE %-12s status=%s threads=%d/%d comments=%d (wanted ~%d) est$%.3f total_est$%.2f %s' % (label, j['tag'], r.get('status'), npo, j['n'], ncm, j['want'], e, state['est'], r.get('err') or ''))

    log('%slaunching %d comment runs, %d at a time' % (label, len(jobs), cfg['workers_comments']))
    with cf.ThreadPoolExecutor(max_workers=cfg['workers_comments']) as ex:
        for f in [ex.submit(run_job, j) for j in jobs]:
            try:
                f.result()
            except Exception as e:
                log('JOB EXCEPTION %r' % e)
    allc = []
    for tag in res:
        p = cfg['out_dir'] + file_prefix + tag + '.json'
        if os.path.exists(p):
            allc.extend(it for it in json.load(open(p, encoding='utf-8')) if it.get('type') == 'comment')
    return allc, res, state['est']


def phase2(cfg, dry):
    rel = Rel(cfg)
    posts = json.load(open(cfg['out_dir'] + 'p1_posts_all.json', encoding='utf-8'))
    log('=== phase 2: %d posts from phase 1, comments budget $%.2f' % (len(posts), cfg['budget_comments']))
    T1, T2, T3 = select_threads(cfg, rel, posts)
    chosen = fit_plan(cfg, T1, T2, T3, cfg['budget_comments'], cfg['schedule'])
    if not chosen:
        log('ABORT: could not fit the budget even with the smallest plan')
        return
    params, sel, est, runs = chosen
    log('CHOSEN %s: threads %d, comments to take %d, runs %d, est $%.2f' % (str(params), len(sel), sum(s[1] for s in sel), runs, est))
    if dry:
        log('DRY RUN: nothing launched')
        return
    json.dump([{'id': s[0].get('id'), 'url': s[0].get('url'), 'subreddit': s[0].get('subreddit'), 'title': s[0].get('title'), 'num_comments': ncom(s[0]), 'take': s[1], 'tier': s[2],
                'cap': s[3], 'created': s[0].get('created_utc')} for s in sel], open(cfg['out_dir'] + 'p2_selection.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    allc, res, spent = run_comment_jobs(cfg, comment_jobs(cfg, sel, 'r'), 'p2_', '')
    json.dump(allc, open(cfg['out_dir'] + 'p2_comments_all.json', 'w', encoding='utf-8'), ensure_ascii=False)
    json.dump(res, open(cfg['out_dir'] + 'p2_results.json', 'w', encoding='utf-8'), indent=1)
    log('=== phase 2 done: comments %d, runs ok %d of %d, estimated spend $%.2f' % (len(allc), sum(1 for v in res.values() if v['status'] == 'SUCCEEDED'), len(res), spent))
    used, limit = A.month_usage()
    log('account monthly usage now %s of limit %s (billing can lag a minute)' % (used, limit))


# ---------- top-up for older windows ----------
def topup(cfg, dry):
    rel = Rel(cfg)
    wins = cfg['topup_windows']
    if not wins:
        log('no topup_windows in the config')
        return
    jobs = []
    for (d0, d1) in wins:
        for g in cfg['query_groups']:
            jobs.append(qjob(cfg, 'w%s_%s' % (d0[:4], g['tag']), g['queries'], min(100, g.get('max_posts', 100)), '0.40', d0, d1))
        for sub in cfg['topup_subs']:
            jobs.append(sjob(cfg, 'w%s_s_%s' % (d0[:4], sub), sub, cfg['topup_sub_keywords'], 50, '0.12', d0, d1))
    log('=== topup: %d post jobs over %d windows, posts budget $%.2f, comments budget $%.2f' % (len(jobs), len(wins), cfg['budget_topup_posts'], cfg['budget_topup_comments']))
    if dry:
        for j in jobs:
            log('DRY %-34s cap $%s  %s' % (j['tag'], j['cap'], ', '.join(j['what'][:5])))
        return
    state = {'est': 0.0}
    res = {}

    def run1(j):
        if state['est'] >= cfg['budget_topup_posts']:
            res[j['tag']] = {'skipped': 'budget'}
            log('SKIP %s (posts budget reached)' % j['tag'])
            return
        r = A.run_and_collect(j['tag'], j['actor'], j['inp'], j['cap'], max_wait=900, timeout_secs=900)
        est = len(r['items']) * cfg['price_post_item']
        with lock:
            state['est'] += est
        with open(cfg['out_dir'] + 'p1b_' + j['tag'] + '.json', 'w', encoding='utf-8') as f:
            json.dump(r['items'], f, ensure_ascii=False)
        res[j['tag']] = {'status': r.get('status'), 'items': len(r['items'])}
        log('1b DONE %-26s status=%s items=%-4d est$%.3f total_est$%.2f %s' % (j['tag'], r.get('status'), len(r['items']), est, state['est'], r.get('err') or ''))

    with cf.ThreadPoolExecutor(max_workers=cfg['workers_posts']) as ex:
        list(ex.map(run1, jobs))
    old = {p['id'] for p in json.load(open(cfg['out_dir'] + 'p1_posts_all.json', encoding='utf-8'))}
    new = {}
    for tag in res:
        p = cfg['out_dir'] + 'p1b_' + tag + '.json'
        if os.path.exists(p):
            for it in json.load(open(p, encoding='utf-8')):
                if it.get('kind') == 'post' and it.get('id') and it['id'] not in old and it['id'] not in new:
                    it['_src'] = tag
                    new[it['id']] = it
    json.dump(list(new.values()), open(cfg['out_dir'] + 'p1b_posts_all.json', 'w', encoding='utf-8'), ensure_ascii=False)
    log('topup posts: new unique posts %d, estimated spend $%.2f' % (len(new), state['est']))
    T1, T2, _ = select_threads(cfg, rel, list(new.values()), 'topup ')
    chosen = fit_plan(cfg, T1, T2, [], cfg['budget_topup_comments'], cfg['topup_schedule'], use_t3=False)
    if not chosen:
        log('topup: nothing fits or nothing selected; stopping')
        return
    params, sel, est, runs = chosen
    allc, res2, spent = run_comment_jobs(cfg, comment_jobs(cfg, sel, 'b'), 'p2b_', '2b ')
    json.dump(allc, open(cfg['out_dir'] + 'p2b_comments_all.json', 'w', encoding='utf-8'), ensure_ascii=False)
    log('=== topup done: new posts %d, comments %d, estimated spend posts $%.2f + comments $%.2f' % (len(new), len(allc), state['est'], spent))
    used, limit = A.month_usage()
    log('account monthly usage now %s of limit %s (billing can lag a minute)' % (used, limit))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--phase', required=True, choices=['1', '2', 'topup'])
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    cfg = load_cfg(a.config)
    LOGF[0] = None if a.dry_run else cfg['out_dir'] + 'pull_log.txt'
    {'1': phase1, '2': phase2, 'topup': topup}[a.phase](cfg, a.dry_run)
