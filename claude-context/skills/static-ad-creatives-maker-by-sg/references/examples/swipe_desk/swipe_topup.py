"""Top up the Swipe Desk pool: fetch the next few brands from brands_backlog.json (Apify, about $0.02 a brand), then rebuild the pool and code the new ads.
  python swipe_topup.py [--brands 6] [--min-room 1.0] [--if-unseen-below 60]
Refuses to run when the Apify room under the monthly limit is below --min-room (the limit is Soumil's and is never raised). Skips brands that returned nothing last time."""
import json, os, re, subprocess, sys, argparse
HERE = os.path.dirname(os.path.abspath(__file__))
SK = 'C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg/scripts'
ap = argparse.ArgumentParser(); ap.add_argument('--brands', type=int, default=6); ap.add_argument('--min-room', type=float, default=1.0); ap.add_argument('--if-unseen-below', type=int, default=0)
a = ap.parse_args()
if a.if_unseen_below:   # daily use: only spend when the pool is running low
    pool = json.load(open(HERE + '/pool/pool_coded.json', encoding='utf-8'))
    seen = set(json.load(open(HERE + '/seen.json', encoding='utf-8')))
    unseen = len([r for r in pool if r['id'] not in seen])
    print('unseen ads in the pool:', unseen)
    if unseen >= a.if_unseen_below:
        print('Pool is healthy (%d >= %d): no top-up today.' % (unseen, a.if_unseen_below)); sys.exit(0)
st = subprocess.run(['python', SK + '/apify_status.py'], capture_output=True, text=True).stdout
m = re.search(r'room left: \$([0-9.]+)', st)
room = float(m.group(1)) if m else 0
print('Apify room left: $%.2f' % room)
if room < a.min_room:
    print('Not enough Apify room (%.2f < %.2f): skipping the top-up, the pool is used as it is.' % (room, a.min_room)); sys.exit(0)
done = set(json.load(open(HERE + '/fetched_brands.json', encoding='utf-8')))
todo = [b for b in json.load(open(HERE + '/brands_backlog.json', encoding='utf-8')) if b['name'] not in done][:a.brands]
if not todo:
    print('Backlog is empty: add brands to brands_backlog.json'); sys.exit(0)
cfg = dict(out=HERE + '/pool', country='US', per_brand=30, today=__import__('datetime').date.today().isoformat(), brands=todo)
json.dump(cfg, open(HERE + '/topup_config.json', 'w', encoding='utf-8'))
subprocess.run(['python', SK + '/competitor_sweep.py', 'fetch', HERE + '/topup_config.json'], check=True)
done.update(b['name'] for b in todo)
json.dump(sorted(done), open(HERE + '/fetched_brands.json', 'w'), indent=1)
# the page-name filter in swipe_pool.py works from fetch_config.json for countries; add the new brands there too
fc = json.load(open(HERE + '/fetch_config.json', encoding='utf-8'))
have = {b['name'] for b in fc['brands']}
fc['brands'] += [b for b in todo if b['name'] not in have]
json.dump(fc, open(HERE + '/fetch_config.json', 'w', encoding='utf-8'), indent=1)
# collision check: print the page names kept for each new brand; a brand whose names are not the brand itself goes into PAGE_ONLY or DROP_BRANDS in swipe_pool.py
import collections, glob
for b in todo:
    fp = HERE + '/pool/brand_%s.json' % re.sub('[^A-Za-z0-9]+', '_', b['name'])
    if os.path.exists(fp):
        d = json.load(open(fp, encoding='utf-8'))
        print('  page names for %s: %s' % (b['name'], dict(collections.Counter(x.get('page_name') for x in d['ads']).most_common(4))))
subprocess.run(['python', HERE + '/swipe_pool.py'], check=True)
subprocess.run(['python', HERE + '/swipe.py', 'code'])   # not fatal: vision coding needs OpenAI credit
print('topped up with', [b['name'] for b in todo])
