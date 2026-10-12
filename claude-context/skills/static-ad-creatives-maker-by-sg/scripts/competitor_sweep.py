"""Competitor ad sweep through the Apify Facebook Ad Library scraper (no browser, no Meta token).

Three steps, run in order:
  fetch   config.json  -> brand_<name>.json per brand (ads sorted by impressions, active only)
  build   config.json  -> index.json + img/ + sheets/ (numbered contact sheets per brand)
  report  config.json  -> reads tags.json (you fill it by looking at the sheets) and prints counts

config.json:
{
 "out": "C:/cca/<brand>/competitors",
 "country": "IN",
 "per_brand": 30,
 "today": "2026-10-04",
 "brands": [ {"name": "Perfora", "role": "direct|leader|adjacent", "industry": "oral care",
              "page_id": "102929252093077" or null, "tokens": ["perfora"], "country": "IN" (optional)} ]
}
tags.json: { "<Brand>": { "<sheet number>": {"bucket": 1-7, "offer": "...", "hook": "...", "fmt": "..."} } }

Rules: Apify token comes from env APIFY_TOKEN (or the Windows user env var). Cost is about $0.04 per brand of 30 ads.
Impressions and spend are NOT available for IN/US commercial ads; run length (start date) is the only winner proxy.
display_format DCO/DPA can hide video: classify by whether any video exists, not by display_format.
Use page_id when you have it (more reliable); else the exact-phrase keyword search is filtered by page-name tokens.
"""
import os, sys, json, re, time, datetime, subprocess, urllib.request, urllib.parse, collections
from concurrent.futures import ThreadPoolExecutor

ACTOR = 'curious_coder~facebook-ads-library-scraper'
BUCKETS = {1: 'Proof (incl. authority)', 2: 'Benefit headline', 3: 'Offer (incl. seasonal / reason-why)', 4: 'Native and atypical',
           5: 'Product hero / lifestyle', 6: 'Explain / mechanism', 7: 'Compare / transform'}


def token():
    t = os.environ.get('APIFY_TOKEN')
    if not t:
        t = subprocess.run(['powershell', '-Command', "[Environment]::GetEnvironmentVariable('APIFY_TOKEN','User')"],
                           capture_output=True, text=True).stdout.strip()
    if not t:
        sys.exit('APIFY_TOKEN not set')
    return t


def slug(s):
    return re.sub('[^A-Za-z0-9]+', '_', s)


def url_for(b, cc):
    base = f"https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={cc}&sort_data[direction]=desc&sort_data[mode]=total_impressions&media_type=all"
    if b.get('page_id'):
        return base + f"&view_all_page_id={b['page_id']}&search_type=page"
    return base + f"&q={urllib.parse.quote(chr(34) + b['name'] + chr(34))}&search_type=keyword_exact_phrase"


def fetch_one(args):
    cfg, b, tok = args
    cc = b.get('country', cfg['country'])
    body = json.dumps({'urls': [{'url': url_for(b, cc)}], 'count': cfg.get('per_brand', 30)}).encode()
    req = urllib.request.Request(f'https://api.apify.com/v2/acts/{ACTOR}/run-sync-get-dataset-items?timeout=280', data=body,
                                 headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json'})
    try:
        d = json.load(urllib.request.urlopen(req, timeout=300))
    except Exception as e:
        return b['name'], 'ERR ' + str(e)[:120]
    toks = [t.lower() for t in b.get('tokens', [b['name'].lower()])]
    keep = d if b.get('page_id') else [x for x in d if any(t in (x.get('page_name') or '').lower() for t in toks)]
    json.dump(dict(brand=b['name'], role=b.get('role'), industry=b.get('industry'), country=cc, ads=keep, fetched=len(d)),
              open(os.path.join(cfg['out'], f"brand_{slug(b['name'])}.json"), 'w'))
    return b['name'], f'fetched {len(d)} kept {len(keep)}' + ('  <- EMPTY: find the page_id and set it' if not keep else '')


def cmd_fetch(cfg):
    os.makedirs(cfg['out'], exist_ok=True)
    tok = token()
    with ThreadPoolExecutor(4) as ex:
        for r in ex.map(fetch_one, [(cfg, b, tok) for b in cfg['brands']]):
            print(*r)


def kind_of(x):
    s = x['snapshot']
    cards = s.get('cards') or []
    hasvid = bool(s.get('videos')) or any(c.get('video_hd_url') or c.get('video_sd_url') for c in cards)
    if s.get('display_format') == 'VIDEO' or hasvid:
        return 'video'
    return 'catalog' if s.get('display_format') == 'DPA' else 'static'


def image_of(x):
    s = x['snapshot']
    if s.get('images'):
        im = s['images'][0]
        return im.get('resized_image_url') or im.get('original_image_url')   # v2.2: resized (about 600 px, 100 KB) is enough for patterns and 10x faster than the 2 MB originals
    for c in s.get('cards') or []:
        u = c.get('resized_image_url') or c.get('original_image_url') or c.get('video_preview_image_url')
        if u:
            return u
    if s.get('videos'):
        return s['videos'][0].get('video_preview_image_url')


def cmd_build(cfg):
    from PIL import Image, ImageDraw, ImageFont
    out = cfg['out']
    today = datetime.datetime.strptime(cfg.get('today', datetime.date.today().isoformat()), '%Y-%m-%d')
    os.makedirs(out + '/img', exist_ok=True)
    os.makedirs(out + '/sheets', exist_ok=True)
    f_big = ImageFont.truetype('arialbd.ttf', 34)
    f_sm = ImageFont.truetype('arial.ttf', 20)
    index, summary = [], []
    for b in cfg['brands']:
        fp = os.path.join(out, f"brand_{slug(b['name'])}.json")
        if not os.path.exists(fp):
            continue
        d = json.load(open(fp, encoding='utf-8'))
        rows, mix, old = [], collections.Counter(), collections.Counter()
        for i, x in enumerate(d['ads']):
            k = kind_of(x)
            try:
                age = (today - datetime.datetime.strptime(x['start_date_formatted'][:10], '%Y-%m-%d')).days
            except Exception:
                age = None
            mix[k] += 1
            if age is not None and age >= 60:
                old[k] += 1
            s = x['snapshot']
            body = (s.get('body') or {}).get('text') or (s.get('cards') or [{}])[0].get('body') or ''
            rows.append(dict(brand=d['brand'], role=d.get('role'), industry=d.get('industry'), ad=x['ad_archive_id'], rank=i + 1, kind=k, age=age,
                             img=image_of(x), title=(s.get('title') or (s.get('cards') or [{}])[0].get('title') or '')[:90],
                             body=body[:200].replace('\n', ' '), cta=s.get('cta_text')))
        statics = sorted([r for r in rows if r['kind'] == 'static' and r['img']], key=lambda r: (0 if (r['age'] or 0) >= 60 else 1, r['rank']))[:20]
        vids = sorted([r for r in rows if r['kind'] == 'video' and r['img']], key=lambda r: -(r['age'] or 0))[:8]
        pick = statics + vids
        def grab(nr):
            n, r = nr
            r['n'] = n
            fn = f"{out}/img/{slug(r['brand'])}_{r['ad']}.jpg"
            if not os.path.exists(fn):
                try:
                    data = urllib.request.urlopen(urllib.request.Request(r['img'], headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()
                    open(fn, 'wb').write(data)
                    Image.open(fn).verify()
                except Exception:
                    fn = None
            r['file'] = fn
        with ThreadPoolExecutor(12) as ex:   # v2.2: parallel downloads (one at a time took about 15 s an image on 2026-10-09)
            list(ex.map(grab, enumerate(pick, 1)))
        cols, W, H = 5, 300, 300
        pk = [r for r in pick if r['file']]
        if pk:
            nrows = (len(pk) + cols - 1) // cols
            sh = Image.new('RGB', (cols * W, nrows * (H + 26) + 40), 'white')
            dr = ImageDraw.Draw(sh)
            dr.text((8, 6), f"{d['brand']} ({d.get('role')}, {d.get('industry')})  mix {dict(mix)}", fill='black', font=f_sm)
            for k, r in enumerate(pk):
                im = Image.open(r['file']).convert('RGB')
                im.thumbnail((W - 6, H - 6))
                x0, y0 = (k % cols) * W, 40 + (k // cols) * (H + 26)
                sh.paste(im, (x0 + 3, y0 + 3))
                dr.rectangle((x0 + 3, y0 + 3, x0 + 48, y0 + 40), fill='orange' if r['kind'] == 'video' else 'red')
                dr.text((x0 + 8, y0 + 4), str(r['n']), fill='white', font=f_big)
                dr.text((x0 + 3, y0 + H + 2), f"{'VIDEO' if r['kind'] == 'video' else 'static'} {r['age']}d", fill='black', font=f_sm)
            sh.save(f"{out}/sheets/{slug(d['brand'])}.jpg", quality=85)
        index.extend(pick)
        summary.append((d['brand'], d.get('role'), len(rows), dict(mix), dict(old)))
    json.dump(index, open(out + '/index.json', 'w'), indent=1)
    for s in summary:
        print(s)
    print('Next: view each sheet, write tags.json, run report.')


def cmd_report(cfg):
    out = cfg['out']
    idx = json.load(open(out + '/index.json'))
    tags = json.load(open(out + '/tags.json'))
    tot, old, per, offers = collections.Counter(), collections.Counter(), collections.defaultdict(collections.Counter), collections.Counter()
    for r in idx:
        t = tags.get(r['brand'], {}).get(str(r['n']))
        if not t:
            continue
        b = t['bucket']
        tot[b] += 1
        per[r['brand']][b] += 1
        if (r['age'] or 0) >= 60:
            old[b] += 1
        if t.get('offer'):
            offers[t['offer']] += 1
    n = sum(tot.values())
    print('tagged', n)
    for b in sorted(tot):
        print(f"{b} {BUCKETS[b]}: {tot[b]} ({round(100 * tot[b] / n)}%), running 60d+: {old[b]}")
    for br, c in per.items():
        print(br, {BUCKETS[k]: v for k, v in c.most_common()})
    print('top offers', offers.most_common(8))


if __name__ == '__main__':
    if len(sys.argv) != 3 or sys.argv[1] not in ('fetch', 'build', 'report'):
        sys.exit(__doc__)
    cfg = json.load(open(sys.argv[2], encoding='utf-8'))
    {'fetch': cmd_fetch, 'build': cmd_build, 'report': cmd_report}[sys.argv[1]](cfg)
