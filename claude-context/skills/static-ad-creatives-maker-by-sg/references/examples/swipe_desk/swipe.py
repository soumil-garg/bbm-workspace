"""Swipe Desk pipeline. One file, five steps (run in order; the daily job runs all of them):
  python swipe.py code                 vision-code the pool (format, hook, offer, devices, headline, idea) with creative_code.py (gpt-5-mini, about $0.0015 an ad)
  python swipe.py batch [--n 30]       pick today's batch from the pool (unseen, mixed brands, countries and buckets) and write batch\\<date>\\
  python swipe.py build                build the review page (swipe_page.html) from the template with today's images embedded
  python swipe.py process decisions.json   turn Soumil's decisions (read from the artifact database) into the library, the log and the taste profile
Folders: pool\\ (brand pulls, pool_index.json, pool\\img), batch\\<date>\\, library.json, decisions_all.json, seen.json.
Library files: C:\\Users\\soumi\\OneDrive\\Desktop\\Ad Inspiration\\Library\\<bucket>\\<format>\\ ; vault notes in Resources\\Ad Inspiration\\ ."""
import json, os, re, sys, io, base64, argparse, random, subprocess, datetime, collections, shutil, urllib.request
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SK = 'C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg/scripts'
TODAY = os.environ.get('SWIPE_TODAY') or datetime.date.today().isoformat()   # SWIPE_TODAY only for dry runs
LIB_ROOT = 'C:/Users/soumi/OneDrive/Desktop/Ad Inspiration/Library'
VAULT = 'C:/Users/soumi/Documents/Vault/Resources/Ad Inspiration'
STATE = HERE
if os.environ.get('SWIPE_TEST'):   # dry run into a scratch folder
    LIB_ROOT = HERE + '/test_out/library'; VAULT = HERE + '/test_out/vault'; STATE = HERE + '/test_out'
BUCKETS = {1: 'Proof and voice of customer', 2: 'Benefit headline', 3: 'Offer and conversion', 4: 'Native and atypical', 5: 'Product hero and lifestyle', 6: 'Explain and mechanism', 7: 'Compare and transform'}
NATIVE_DEV = {'chat_bubbles', 'notes_or_list_app', 'search_box', 'receipt_or_ledger', 'weather_or_app_widget', 'handwritten_or_sticky_note', 'humour_wordplay_or_spoof'}
OFFER_DEV = {'price_sticker_or_burst', 'free_gift_badge', 'discount_badge', 'urgency_label'}
PROOF_DEV = {'review_stars_or_quote', 'customer_count_claim'}
FMT_NAME = {'product_hero': 'Product shot', 'lifestyle_scene': 'Scene', 'ugc_or_creator_photo': 'Creator photo', 'fake_screen': 'Fake screen', 'typographic_offer': 'Text offer',
            'explainer_or_infographic': 'Explainer', 'comparison_or_before_after': 'Comparison', 'testimonial_or_review_card': 'Review card', 'multi_product_collage': 'Range',
            'meme_or_humour': 'Humour', 'other': 'Other'}


def jload(p, default=None):
    return json.load(open(p, encoding='utf-8')) if os.path.exists(p) else default


def jsave(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)


def bucket_of(r):
    dev = set(r.get('devices') or [])
    f, h, o = r.get('format'), r.get('hook'), r.get('offer')
    if f == 'comparison_or_before_after' or 'before_after_split' in dev:
        return 7
    if f in ('fake_screen', 'meme_or_humour') or dev & NATIVE_DEV:
        return 4
    if f == 'testimonial_or_review_card' or h in ('social_proof', 'authority') or dev & PROOF_DEV:
        return 1
    if (o and o != 'none') or h in ('offer_price', 'scarcity_urgency') or dev & OFFER_DEV or f == 'typographic_offer':
        return 3
    if f == 'explainer_or_infographic' or h == 'how_to_demo' or 'checklist_ticks' in dev:
        return 6
    if h == 'benefit' and f in ('product_hero', 'lifestyle_scene'):
        return 2
    if f == 'ugc_or_creator_photo':
        return 4
    return 5


def cmd_code(a):
    pool = jload(HERE + '/pool/pool_index.json', [])
    idx = []
    for k, r in enumerate(pool, 1):
        idx.append(dict(brand=r['brand'], ad=r['ad'], n=k, kind='static', age=r['age'], role='best', industry='', title=r.get('title') or '', body=r.get('body') or '', cta=r.get('cta') or '', file=r['file']))
    jsave(HERE + '/pool/index_for_code.json', idx)
    cmd = ['python', SK + '/creative_code.py', 'code', '--index', HERE + '/pool/index_for_code.json', '--out', HERE + '/pool/coded.json', '--about',
           'Meta static ads from well-known D2C and consumer brands in India and the US', '--workers', '10', '--model', 'gpt-5-mini', '--effort', 'low']
    r = subprocess.run(cmd)
    if r.returncode != 0:
        print('WARNING: vision coding failed (OpenAI credit or network); continuing with the ads that are already coded')
    coded = {(c['brand'], str(c['ad'])): c for c in jload(HERE + '/pool/coded.json', [])}
    out = []
    for r in pool:
        c = coded.get((r['brand'], str(r['ad'])))
        if not c:
            continue
        r.update(format=c['format'], hook=c['hook'], offer=c['offer'], devices=c.get('devices', []), headline=re.sub(r'\s+', ' ', c.get('headline_text') or '').strip(), idea=c.get('idea'),
                 people=c.get('people'), text_amount=c.get('text_amount'), palette=c.get('palette'), claims=c.get('claims', []))
        r['bucket'] = bucket_of(r)
        out.append(r)
    jsave(HERE + '/pool/pool_coded.json', out)
    print('coded pool:', len(out), dict(collections.Counter(BUCKETS[r['bucket']] for r in out)))


def ui_image(r, folder):
    """full-size image for the review (the original when available, about 900 px) and a small thumb for the history grid"""
    fn = '%s/%s.jpg' % (folder, r['id'])
    if not os.path.exists(fn):
        for u in (r.get('img_big'), r.get('img_small')):
            if not u:
                continue
            try:
                data = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=40).read()
                open(fn + '.orig', 'wb').write(data)
                Image.open(fn + '.orig').verify()
                break
            except Exception:
                if os.path.exists(fn + '.orig'):
                    os.remove(fn + '.orig')
                continue
        else:
            return None
        im = Image.open(fn + '.orig').convert('RGB')
        im.thumbnail((900, 900))
        im.save(fn, 'JPEG', quality=80)
    return fn


VARIETY_FORMATS = {'ugc_or_creator_photo', 'fake_screen', 'meme_or_humour'}


def is_variety(r):
    """native, humour, creator-photo or people-led: the kinds the library is thin on (10 Oct 2026)"""
    return r.get('bucket') == 4 or r.get('format') in VARIETY_FORMATS or r.get('people') in ('one_person', 'two_plus')


def spaced(items, rnd):
    """order a queue so the same brand never shows twice within 4 ads and the countries alternate where possible"""
    pool = items[:]
    rnd.shuffle(pool)
    out, recent = [], []
    while pool:
        pick = None
        for mode in (0, 1, 2):
            for i, r in enumerate(pool):
                ok_brand = r['brand'] not in recent[-3:]
                ok_cty = not out or r['country'] != out[-1]['country']
                if (mode == 0 and ok_brand and ok_cty) or (mode == 1 and ok_brand) or mode == 2:
                    pick = i
                    break
            if pick is not None:
                break
        r = pool.pop(pick)
        out.append(r)
        recent.append(r['brand'])
    return out


def cmd_batch(a):
    """The queue (endless since 10 Oct 2026): every ad of the last queue that is still undecided, then new ones from the pool up to --n,
    spaced by brand and country. Run `process` first so decisions_all.json is current."""
    pool = jload(HERE + '/pool/pool_coded.json', [])
    seen = set(jload(HERE + '/seen.json', []))
    dec_ids = set(jload(STATE + '/decisions_all.json', {}).keys())
    rnd = random.Random(TODAY)
    bdir = HERE + '/batch'
    prev = [f for f in sorted(os.listdir(bdir)) if f <= TODAY] if os.path.isdir(bdir) else []
    carry, have = [], set()
    if prev:
        for i in jload('%s/%s/batch.json' % (bdir, prev[-1]), []):
            if i['id'] not in dec_ids and i['id'] not in have and os.path.exists(i['file']):
                carry.append(i)
                have.add(i['id'])
    carry = carry[:a.n]
    need = a.n - len(carry)
    cand = [r for r in pool if r['id'] not in seen and r['id'] not in dec_ids and r['id'] not in have]
    for r in cand:
        r['score'] = min(r['age'], 365) / 365.0 + rnd.random() * 0.4
    for r in cand:
        if is_variety(r):
            r['score'] += 1.0   # fill the queue with the kinds the library is thin on first
    cand.sort(key=lambda r: -r['score'])
    by = {'IN': [r for r in cand if r['country'] == 'IN'], 'US': [r for r in cand if r['country'] != 'IN']}
    per_brand = collections.Counter(i['brand'] for i in carry)
    chosen, t = [], 0
    for cap in (14, 999):   # at most 14 ads a brand in the queue, relaxed only if the pool is thin
        pos = {'IN': 0, 'US': 0}
        taken = {r['id'] for r in chosen}
        by = {k: [r for r in v if r['id'] not in taken] for k, v in by.items()}
        while len(chosen) < need and (pos['IN'] < len(by['IN']) or pos['US'] < len(by['US'])):
            c = ('IN', 'US')[t % 2]
            t += 1
            while pos[c] < len(by[c]) and per_brand[by[c][pos[c]]['brand']] >= cap:
                pos[c] += 1
            if pos[c] < len(by[c]):
                r = by[c][pos[c]]
                pos[c] += 1
                chosen.append(r)
                per_brand[r['brand']] += 1
        if len(chosen) >= need:
            break
    folder = HERE + '/batch/' + TODAY
    os.makedirs(folder, exist_ok=True)
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(8) as ex:
        files = list(ex.map(lambda r: ui_image(r, folder), chosen))
    new = []
    for r, fn in zip(chosen, files):
        if not fn:
            continue
        why = 'Running %d days. A long-running ad is a survival signal, not proof that it sells.' % r['age']
        new.append(dict(id=r['id'], brand=r['brand'], country=r['country'], days=r['age'], format=r['format'], hook=r['hook'], offer=r['offer'], bucket=r['bucket'],
                        headline=r['headline'], people=r.get('people'), ad=r['ad'], link=r['link'], title=('' if '{{' in (r.get('title') or '') else r.get('title')),
                        body=('' if '{{' in (r.get('body') or '') else (r.get('body') or '')[:300]), why=why, file=fn, batch=TODAY))
    allq = carry + new
    prio = [r for r in allq if is_variety(r)]
    rest = [r for r in allq if not is_variety(r)]
    prio, rest = spaced(prio, rnd), spaced(rest, rnd)
    items, pi, ri = [], 0, 0   # one native or people-led ad in every three, until they run out
    while pi < len(prio) or ri < len(rest):
        if pi < len(prio) and (len(items) % 3 == 0 or ri >= len(rest)):
            items.append(prio[pi]); pi += 1
        elif ri < len(rest):
            items.append(rest[ri]); ri += 1
        else:
            items.append(prio[pi]); pi += 1
    jsave(folder + '/batch.json', items)
    print('queue %s: %d ads (%d carried over undecided, %d new), %d brands, %s, buckets %s' % (TODAY, len(items), len(carry), len(new), len(set(i['brand'] for i in items)),
                                                                                              dict(collections.Counter(i['country'] for i in items)), dict(collections.Counter(BUCKETS[i['bucket']] for i in items))))
    used = {i['id'] for i in items}
    print('pool left unseen after this queue:', len([r for r in pool if r['id'] not in seen and r['id'] not in dec_ids and r['id'] not in used]))


def data_uri(fn, side=None, q=80):
    im = Image.open(fn).convert('RGB')
    if side:
        im.thumbnail((side, side))
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=q)
    return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()


def webp_uri(fn, side=720, q=72):
    im = Image.open(fn).convert('RGB')
    im.thumbnail((side, side))
    buf = io.BytesIO()
    im.save(buf, 'WEBP', quality=q)
    return 'data:image/webp;base64,' + base64.b64encode(buf.getvalue()).decode()


def cmd_build(a):
    import glob
    folder = HERE + '/batch/' + TODAY
    items = jload(folder + '/batch.json', [])
    idx = {}   # every image of every earlier queue, for the history thumbnails
    for fdr in sorted(os.listdir(HERE + '/batch')):
        for fn in glob.glob('%s/batch/%s/*.jpg' % (HERE, fdr)):
            idx[os.path.basename(fn)[:-4]] = fn
    tmpl = open(HERE + '/swipe_ui.tmpl.html', encoding='utf-8').read()
    js = lambda o: json.dumps(o, ensure_ascii=True).replace('</', '<\\/')
    dec = jload(STATE + '/decisions_all.json', {})
    queue_ids = {i['id'] for i in items}
    thumbs = {}
    for d in sorted(dec.values(), key=lambda d: d.get('at', ''), reverse=True)[:150]:
        if d['id'] not in queue_ids and idx.get(d['id']):
            thumbs[d['id']] = webp_uri(idx[d['id']], 200, 60)
    for side, q in ((720, 72), (640, 66), (560, 60)):   # the page must stay under about 15 MB
        batch = []
        for i in items:
            d = {k: v for k, v in i.items() if k != 'file'}
            d['img'] = webp_uri(i['file'], side, q)
            batch.append(d)
        html = tmpl.replace('/*BATCH_JSON*/[]', js(batch)).replace('/*THUMBS_JSON*/{}', js(thumbs)).replace('/*BATCH_DATE*/', TODAY)
        if len(html.encode('utf-8')) < 15.0e6:
            break
    open(HERE + '/swipe_page.html', 'w', encoding='utf-8').write(html)
    print('page built: %.1f MB, %d ads in the queue (images %d px), %d history thumbs' % (len(html.encode('utf-8')) / 1e6, len(batch), side, len(thumbs)))
    seen = set(jload(HERE + '/seen.json', []))
    seen.update(i['id'] for i in items)
    jsave(HERE + '/seen.json', sorted(seen))
    jsave(HERE + '/queue_built.json', dict(date=TODAY, ids=[i['id'] for i in items]))


def cmd_mark_published(a):
    """run right after the page was published: the live page now holds exactly the queue that was last built"""
    qb = jload(HERE + '/queue_built.json', {})
    qb['published_at'] = datetime.datetime.now().isoformat(timespec='seconds')
    jsave(HERE + '/published.json', qb)
    print('published.json: %d ads on the live page' % len(qb.get('ids', [])))


def cmd_last_at(a):
    """newest decision time already processed; pull only decisions after it (ArtifactData query where at > this)"""
    allx = jload(STATE + '/decisions_all.json', {})
    print(max([d.get('at', '') for d in allx.values()] or ['1970-01-01T00:00:00.000Z']))


def collect(dirpath):
    import glob
    rows = []
    for fp in glob.glob(dirpath.rstrip('/\\') + '/*.json'):
        d = json.load(open(fp, encoding='utf-8'))
        rows.append(d.get('data', d))
    return rows


def cmd_refill(a):
    """The daily job in one call: process the pulled decisions, then rebuild the page only if the live one is running low.
    Prints PUBLISH: yes or no. After a yes: publish swipe_page.html to the artifact, then run `mark_published`."""
    if a.pulled:
        rows = collect(a.pulled)
        tmp = HERE + '/db_pull/_collected.json'
        jsave(tmp, rows)
        cmd_process(argparse.Namespace(file=tmp))
    dec_ids = set(jload(STATE + '/decisions_all.json', {}).keys())
    pub = jload(HERE + '/published.json', {})
    left = [i for i in pub.get('ids', []) if i not in dec_ids]
    print('live page: %d ads published, %d still undecided' % (len(pub.get('ids', [])), len(left)))
    if not a.force and len(left) >= a.min_left:
        print('PUBLISH: no (the live page still has %d undecided ads, threshold %d)' % (len(left), a.min_left))
        return
    subprocess.run(['python', HERE + '/swipe_topup.py', '--if-unseen-below', str(a.pool_low)])
    cmd_code(None)
    cmd_batch(argparse.Namespace(n=a.n))
    cmd_build(None)
    print('PUBLISH: yes. Page file: %s/swipe_page.html' % HERE.replace('\\', '/'))


# ------------------------------------------------------------------ process decisions into the library
def vision_fields(r, fn):
    """principle, brand-agnostic template, funnel, awareness for an approved ad (gpt-5-mini, about $0.003)"""
    sys.path.insert(0, SK)
    from theme_counter import getenv
    key = getenv('OPENAI_API_KEY')
    if not key:
        return {}
    im = Image.open(fn).convert('RGB'); im.thumbnail((1024, 1024))
    buf = io.BytesIO(); im.save(buf, 'JPEG', quality=85)
    b64 = base64.b64encode(buf.getvalue()).decode()
    schema = {'type': 'object', 'properties': {
        'principle': {'type': 'string'}, 'template': {'type': 'string'},
        'funnel': {'type': 'string', 'enum': ['TOF', 'MOF', 'BOF']},
        'awareness': {'type': 'string', 'enum': ['unaware', 'problem aware', 'solution aware', 'product aware', 'most aware']}},
        'required': ['principle', 'template', 'funnel', 'awareness'], 'additionalProperties': False}
    ask = ('This Meta static ad was approved by an ad buyer for his swipe file. In one plain sentence say why the layout and words work (principle). Then give a brand-agnostic TEMPLATE: the structure with square-bracket '
           'placeholders, e.g. "[Number] + [thing]. [Short qualifier]. Big product shot on [solid colour], sticker top right". Then funnel stage and the awareness level it speaks to. No hype words. Ad text from the feed: '
           + (r.get('title') or '') + ' | ' + (r.get('body') or ''))
    body = json.dumps({'model': 'gpt-5-mini', 'messages': [{'role': 'user', 'content': [{'type': 'text', 'text': ask}, {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + b64, 'detail': 'high'}}]}],
                       'response_format': {'type': 'json_schema', 'json_schema': {'name': 'lib', 'strict': True, 'schema': schema}}, 'reasoning_effort': 'low', 'max_completion_tokens': 3000}).encode()
    req = urllib.request.Request('https://api.openai.com/v1/chat/completions', data=body, headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=120).read().decode())
        return json.loads(d['choices'][0]['message']['content'])
    except Exception as e:
        print('vision fields failed for', r['id'], str(e)[:100])
        return {}


def write_notes(lib, allx):
    # Library note
    L = ['---', 'date: %s' % TODAY, 'tags: [resource, business/creatives, inspiration-library]', 'status: active', '---', '', '# Inspiration library (approved in Swipe Desk)', '',
         'Built from Soumil\'s approvals of well-known brands\' statics. Files: `C:\\Users\\soumi\\OneDrive\\Desktop\\Ad Inspiration\\Library\\<bucket>\\<format>\\`. Plan and schema: [[inspiration-library-plan]]. Taste read: [[Swipe Taste Profile]]. ',
         'Buckets follow [[competitor-sweep-oct2026]]; the bucket, format and hook are model-tagged and checked by Soumil\'s approval, not by eye.', '']
    byb = collections.defaultdict(list)
    for e in lib.values():
        byb[e['bucket']].append(e)
    for b in sorted(byb):
        L += ['## %d. %s (%d)' % (b, BUCKETS[b], len(byb[b])), '', '| Brand | Format | Funnel | Awareness | Days | Why it works | Template | Soumil | File |', '|---|---|---|---|---|---|---|---|---|']
        for e in sorted(byb[b], key=lambda e: e['approved_at']):
            L.append('| %s (%s) | %s | %s | %s | %s | %s | %s | %s | `%s` |' % (e['brand'], e['country'], FMT_NAME.get(e['format'], e['format']), e.get('funnel', ''), e.get('awareness', ''), e['days'],
                                                                    (e.get('principle') or '').replace('|', '/'), (e.get('template') or '').replace('|', '/'), ((e.get('note') or '') + (' [' + ', '.join(e.get('tags') or []) + ']' if e.get('tags') else '')).replace('|', '/'), os.path.relpath(e['library_file'], 'C:/Users/soumi/OneDrive/Desktop/Ad Inspiration')))
        L.append('')
    maybe = [d for d in allx.values() if d['decision'] == 'maybe']
    L += ['## Maybe pile (%d)' % len(maybe), '', 'Look again after 14 days; promote or drop.', '', '| Brand | Format | Decided | Note | Ad Library |', '|---|---|---|---|---|']
    for d in sorted(maybe, key=lambda d: d['at']):
        L.append('| %s | %s | %s | %s | %s |' % (d['brand'], FMT_NAME.get(d.get('format'), d.get('format')), d['at'][:10], (d.get('note') or '').replace('|', '/'), d.get('link') or ''))
    open(VAULT + '/Inspiration Library.md', 'w', encoding='utf-8').write('\n'.join(L) + '\n')

    # Taste profile
    A = list(allx.values())
    def rate(keyf, minn=2):
        m = collections.defaultdict(lambda: collections.Counter())
        for d in A:
            k = keyf(d)
            if k:
                m[k][d['decision']] += 1
        rows = []
        for k, c in m.items():
            n = sum(c.values())
            if n >= minn:
                rows.append((k, n, c['approve'], c['reject'], c['maybe'], c['other']))
        return sorted(rows, key=lambda r: (-(r[2] / r[1]), -r[1]))
    T = ['---', 'date: %s' % TODAY, 'tags: [resource, business/creatives, taste]', 'status: active', '---', '', '# Swipe taste profile', '',
         'Updated each time decisions are processed. %d decisions so far: %d approved, %d disapproved, %d maybe, %d with a note. Use it in Stage 4 (copy) and Stage 5 (design) of the ad skill: lean toward high-approval formats, hooks and brands, and read the comments first. Small samples, so read as direction only.' % (
            len(A), sum(d['decision'] == 'approve' for d in A), sum(d['decision'] == 'reject' for d in A), sum(d['decision'] == 'maybe' for d in A), sum(d['decision'] == 'other' for d in A)), '']
    for title, kf in (('By format', lambda d: FMT_NAME.get(d.get('format'), d.get('format'))), ('By bucket', lambda d: BUCKETS.get(d.get('bucket'))), ('By hook', lambda d: (d.get('hook') or '').replace('_', ' ')),
                      ('By country', lambda d: d.get('country')), ('By brand', lambda d: d.get('brand'))):
        T += ['## ' + title, '', '| Value | n | approved | disapproved | maybe | note | approval rate |', '|---|---|---|---|---|---|---|']
        for k, n, ap, rj, mb, ot in rate(kf):
            T.append('| %s | %d | %d | %d | %d | %d | %d%% |' % (k, n, ap, rj, mb, ot, round(100 * ap / n)))
        T.append('')
    tg = collections.Counter()
    for d in A:
        for t in d.get('tags') or []:
            tg[(t, d['decision'])] += 1
    T += ['## What drives it (reasons ticked)', '', ', '.join('%s (%s) %d' % (t, dec, n) for (t, dec), n in tg.most_common(20)) or 'none yet', '', '## His words (notes, newest first)', '']
    for d in sorted([d for d in A if d.get('note')], key=lambda d: d['at'], reverse=True)[:60]:
        T.append('- %s, %s, %s: "%s"' % (d['brand'], d['decision'], d.get('headline') or '', d['note'].replace('\n', ' ')))
    open(VAULT + '/Swipe Taste Profile.md', 'w', encoding='utf-8').write('\n'.join(T) + '\n')


def cmd_process(a):
    new = json.load(open(a.file, encoding='utf-8'))
    if isinstance(new, dict) and 'docs' in new:
        new = new['docs']
    new = [d.get('data', d) if isinstance(d, dict) else d for d in new]
    allx = jload(STATE + '/decisions_all.json', {})
    lib = jload(STATE + '/library.json', {})
    for d in new:
        allx[d['id']] = d
    pool = {r['id']: r for r in jload(HERE + '/pool/pool_coded.json', [])}
    added = 0
    for id_, d in allx.items():
        if d['decision'] != 'approve' or id_ in lib:
            continue
        r = pool.get(id_) or {}
        batch_img = None
        for fdr in sorted(os.listdir(HERE + '/batch'), reverse=True):
            p = '%s/batch/%s/%s.jpg' % (HERE, fdr, id_)
            if os.path.exists(p):
                batch_img = p; break
        src = batch_img or r.get('file')
        if not src or not os.path.exists(src):
            print('no image for', id_); continue
        bucket = d.get('bucket') or r.get('bucket') or 5
        fmt = d.get('format') or r.get('format') or 'other'
        folder = '%s/%d %s/%s' % (LIB_ROOT, bucket, BUCKETS[bucket], FMT_NAME.get(fmt, fmt))
        os.makedirs(folder, exist_ok=True)
        dst = '%s/%s.jpg' % (folder, id_)
        shutil.copy(src, dst)
        extra = vision_fields(dict(r, **{'title': r.get('title'), 'body': r.get('body')}), dst)
        lib[id_] = dict(id=id_, brand=d['brand'], country=d.get('country'), days=d.get('days'), format=fmt, hook=d.get('hook'), bucket=bucket, headline=d.get('headline'), link=d.get('link'),
                        note=d.get('note'), tags=d.get('tags'), approved_at=d['at'], library_file=dst, **extra)
        added += 1
    jsave(STATE + '/library.json', lib)
    jsave(STATE + '/decisions_all.json', allx)
    os.makedirs(VAULT, exist_ok=True)
    write_notes(lib, allx)
    print('processed: %d decisions in total, %d new library entries, library now %d' % (len(allx), added, len(lib)))


if __name__ == '__main__':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('code')
    p = sub.add_parser('batch'); p.add_argument('--n', type=int, default=200)
    sub.add_parser('build')
    p = sub.add_parser('process'); p.add_argument('file')
    sub.add_parser('mark_published')
    sub.add_parser('last_at')
    p = sub.add_parser('refill'); p.add_argument('--pulled'); p.add_argument('--n', type=int, default=200); p.add_argument('--min-left', type=int, default=100)
    p.add_argument('--pool-low', type=int, default=150); p.add_argument('--force', action='store_true')
    a = ap.parse_args()
    {'code': cmd_code, 'batch': cmd_batch, 'build': cmd_build, 'process': cmd_process, 'mark_published': cmd_mark_published, 'last_at': cmd_last_at, 'refill': cmd_refill}[a.cmd](a)
