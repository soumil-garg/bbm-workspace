"""Swipe pool: turn the Apify Ad Library pulls of the 'best statics' brands into a clean pool of static ads (resized images, one record per ad).
  python swipe_pool.py [--min-age 30] [--per-brand 8]
Inputs: pool\\brand_*.json (this folder, fetched with competitor_sweep.py fetch) and C:\\cca\\adlib\\brand_*.json (the 4 Oct sweep).
Rules: genuine statics only (no video, no catalog or DPA), running at least --min-age days (default 14), one record per creative (collation id), near-duplicate images dropped,
onboarded client brands excluded (onboarded.json), at most --per-brand per brand, the longest-running first. Output: pool\\pool_index.json and pool\\img\\<id>.jpg (about 600 px).
Run length is only a survival proxy: IN and US commercial ads show no spend or impressions."""
import json, os, re, sys, glob, datetime, argparse, urllib.request, importlib.util
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SK = 'C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg/scripts/competitor_sweep.py'
spec = importlib.util.spec_from_file_location('cs', SK)
cs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cs)

ap = argparse.ArgumentParser()
ap.add_argument('--min-age', type=int, default=14)   # 10 Oct: was 30; the page shows 'running N days' and the queue prefers the older ads
ap.add_argument('--per-brand', type=int, default=30)  # 10 Oct: was 8; the queue spaces brands apart, so a deep pool is fine
a = ap.parse_args()
TODAY = datetime.date.today()
ONB = [x.lower() for x in json.load(open(HERE + '/onboarded.json', encoding='utf-8'))]
os.makedirs(HERE + '/pool/img', exist_ok=True)
COUNTRY = {}
for b in json.load(open(HERE + '/fetch_config.json', encoding='utf-8'))['brands']:
    COUNTRY[b['name'].lower()] = b['country']


def slug(s):
    return re.sub('[^A-Za-z0-9]+', '_', s).strip('_')


def dhash(path):
    im = Image.open(path).convert('L').resize((9, 8))
    px = list(im.getdata())
    bits = 0
    for r in range(8):
        for c in range(8):
            bits = (bits << 1) | (1 if px[r * 9 + c] > px[r * 9 + c + 1] else 0)
    return bits


def best_img(x, kind):
    s = x['snapshot']
    rows = []
    if s.get('images'):
        rows.append(s['images'][0])
    for c in s.get('cards') or []:
        rows.append(c)
    for im in rows:
        r, o = im.get('resized_image_url'), im.get('original_image_url')
        if r or o:
            return r or o, o or r
    return None, None


# name collisions seen on 9 Oct (the Ad Library search is by name): only these exact page names count for ambiguous brands; the others are dropped
PAGE_ONLY = {'cred': {'cred'}, 'casper': {'casper'}, 'harrys': {"harry's"}, 'poppi': {'poppi'}}
DROP_BRANDS = {'prime hydration', 'recess', 'ridge', 'blinkit', 'chaayos', 'virasat-e-curry'}
recs = []
ADLIB_OK = ['sleepy owl', 'mamaearth', 'minimalist', 'bombay shaving company', 'the whole truth', 'perfora', 'beardo', 'sorry sugar', 'farmley']   # the 4 Oct sweep: only brands that belong on a best-statics list
EXTRA = glob.glob('C:/cca/daigo/competitors/brand_*.json')   # 10 Oct: the Daigo competitor pulls (native, humour and people-led statics); Daigo's own file is dropped by onboarded.json
files = glob.glob(HERE + '/pool/brand_*.json') + EXTRA + [f for f in glob.glob('C:/cca/adlib/brand_*.json') if os.path.basename(f)[6:-5].replace('_', ' ').lower() in ADLIB_OK]
seen_ads = set()
for fp in files:
    d = json.load(open(fp, encoding='utf-8'))
    brand = d['brand']
    if any(o in brand.lower() for o in ONB):
        continue
    toks = [t.lower() for t in [brand.lower()]]
    for x in d['ads']:
        aid = x['ad_archive_id']
        if aid in seen_ads:
            continue
        seen_ads.add(aid)
        try:
            kind = cs.kind_of(x)
        except Exception:
            continue
        if kind != 'static':
            continue
        try:
            age = (TODAY - datetime.datetime.strptime(x['start_date_formatted'][:10], '%Y-%m-%d').date()).days
        except Exception:
            continue
        if age < a.min_age:
            continue
        r, o = best_img(x, kind)
        if not r:
            continue
        pn = (x.get('page_name') or '').lower()
        if brand.lower() in DROP_BRANDS or (brand.lower() in PAGE_ONLY and pn not in PAGE_ONLY[brand.lower()]):
            continue
        s = x['snapshot']
        m = re.search(r'country=([A-Z]{2})', x.get('url') or '')
        country = COUNTRY.get(brand.lower()) or (m.group(1) if m else '')
        body = ((s.get('body') or {}).get('text') or '').replace('\n', ' ')
        recs.append(dict(id='%s_%s' % (slug(brand), aid), brand=brand, page=x.get('page_name'), country=country, age=age, ad=aid, collation=x.get('collation_id') or aid,
                         copies=x.get('collation_count') or 1, title=(s.get('title') or '')[:120], body=body[:300], cta=s.get('cta_text'), link=x.get('ad_library_url'),
                         landing=s.get('link_url'), img_small=r, img_big=o))
print('static candidates after age filter:', len(recs), 'from', len(files), 'files')

# one per creative (collation id), longest running first, capped per brand
by = {}
for r in sorted(recs, key=lambda r: -r['age']):
    by.setdefault(r['brand'], []).append(r)
keep = []
for b, rs in by.items():
    seen_c = set()
    n = 0
    for r in rs:
        if r['collation'] in seen_c:
            continue
        seen_c.add(r['collation'])
        keep.append(r)
        n += 1
        if n >= a.per_brand * 2:   # a margin: near-duplicates are dropped after the download
            break
print('after collation and per-brand margin:', len(keep))


def grab(r):
    fn = HERE + '/pool/img/%s.jpg' % r['id']
    if not os.path.exists(fn):
        try:
            data = urllib.request.urlopen(urllib.request.Request(r['img_small'], headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()
            open(fn, 'wb').write(data)
            Image.open(fn).verify()
        except Exception:
            if os.path.exists(fn):
                os.remove(fn)
            return None
    r['file'] = fn
    return r


with ThreadPoolExecutor(12) as ex:
    got = [r for r in ex.map(grab, keep) if r]
print('downloaded:', len(got))
# near-duplicate images within a brand, then the per-brand cap
final = []
for b in sorted(set(r['brand'] for r in got)):
    hs = []
    n = 0
    for r in sorted([r for r in got if r['brand'] == b], key=lambda r: -r['age']):
        try:
            h = dhash(r['file'])
        except Exception:
            continue
        if any(bin(h ^ g).count('1') <= 6 for g in hs):
            continue
        hs.append(h)
        final.append(r)
        n += 1
        if n >= a.per_brand:
            break
json.dump(final, open(HERE + '/pool/pool_index.json', 'w', encoding='utf-8'), indent=1)
import collections
print('pool:', len(final), 'ads from', len(set(r['brand'] for r in final)), 'brands |', dict(collections.Counter(r['country'] for r in final)))
print(collections.Counter(r['brand'] for r in final).most_common(12))
