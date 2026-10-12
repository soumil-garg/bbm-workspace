"""Vision-code competitor ads (v2.2): read the PICTURE of every ad, count the patterns, build numbered sheets for any cluster.
Works on the index.json written by competitor_sweep.py build (one row per ad with the downloaded image in `file`).

  python creative_code.py code  --index C:/cca/<brand>/competitors/index.json --out C:/cca/<brand>/competitors/coded.json --about "Meta ads from Indian D2C food and drink brands"
  python creative_code.py count --index ... --coded ... --report C:/cca/<brand>/competitors/pattern_counts.md
  python creative_code.py sheet --index ... --coded ... --field format --value fake_screen --out C:/cca/<brand>/competitors/sheets/cluster_native_mock.jpg
  python creative_code.py audit --index ... --coded ... --out C:/cca/<brand>/competitors/audit   (60 random ads, numbered sheets without the model tags, for a by-eye check)

Cost: about $0.002 an ad (gpt-5-mini, image at high detail, reasoning low; prices assumed $0.25 in and $2.00 out per M tokens). 450 ads is about $1.
OPENAI_API_KEY comes from the user environment and is never printed. Tags are made by a model reading the picture: audit them by eye (the `audit` command) before quoting counts.
Run with the system python (needs PIL), not `python -I`.
"""
import sys, os, json, io, base64, argparse, time, collections, threading, random
from concurrent.futures import ThreadPoolExecutor
import urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme_counter import getenv

MODEL = 'gpt-5-mini'
ENUMS = {
    'format': ['product_hero', 'lifestyle_scene', 'ugc_or_creator_photo', 'fake_screen', 'typographic_offer', 'explainer_or_infographic',
               'comparison_or_before_after', 'testimonial_or_review_card', 'multi_product_collage', 'meme_or_humour', 'other'],
    'hook': ['benefit', 'curiosity', 'offer_price', 'social_proof', 'problem_pain', 'how_to_demo', 'nostalgia_home', 'identity_status',
             'scarcity_urgency', 'authority', 'none'],
    'offer': ['none', 'price_point', 'percent_off', 'bundle_deal', 'free_shipping', 'free_trial_or_sample', 'discount_code', 'other'],
    'product_visibility': ['none', 'small', 'medium', 'hero'],
    'people': ['none', 'hands_only', 'one_person', 'two_plus'],
    'setting': ['plain_studio', 'home_kitchen', 'travel_transit', 'office_work', 'outdoors_nature', 'gym_sports', 'cafe_restaurant', 'abstract_graphic', 'other'],
    'text_amount': ['none', 'little', 'medium', 'heavy'],
    'headline_language': ['english', 'hinglish', 'hindi', 'none'],
}
DEVICES = ['chat_bubbles', 'notes_or_list_app', 'search_box', 'receipt_or_ledger', 'weather_or_app_widget', 'handwritten_or_sticky_note', 'letter_board_or_signage', 'crossed_out_text',
           'checklist_ticks', 'before_after_split', 'review_stars_or_quote', 'customer_count_claim', 'price_sticker_or_burst', 'free_gift_badge', 'discount_badge', 'urgency_label',
           'humour_wordplay_or_spoof', 'creator_or_celebrity_face', 'mascot_or_animation', 'hand_holding_product', 'pour_or_splash', 'none']
COARSE = {'product_hero': 'product_led', 'multi_product_collage': 'product_led', 'typographic_offer': 'text_card', 'explainer_or_infographic': 'text_card',
          'testimonial_or_review_card': 'text_card', 'comparison_or_before_after': 'text_card', 'lifestyle_scene': 'people_scene', 'ugc_or_creator_photo': 'people_scene',
          'fake_screen': 'fake_screen', 'meme_or_humour': 'humour', 'other': 'other'}   # the 6 groups that agreed 80%+ with a by-eye audit
CLAIMS = ['taste', 'convenience_speed', 'health_gut', 'protein_nutrition', 'natural_clean', 'price_value', 'desi_nostalgia', 'travel_portability', 'energy_hydration', 'other']
RULES = """You code ONE Meta (Facebook and Instagram) ad from India for a research study on %s.
You see the ad image and the ad's text fields. Describe only what is visible or written. Never judge quality and never guess performance.
format: choose the ONE that best describes the picture. fake_screen = the main visual IS a screenshot-style imitation of a phone, app, chat (bubbles), notes list, tweet, search box, email, receipt or spreadsheet; a product photo with a headline is NEVER fake_screen and a person holding a phone is not fake_screen. testimonial_or_review_card = a customer quote, star rating or review text is the main element. meme_or_humour = a joke, spoof or meme framing is the main element. comparison_or_before_after = two things or two states side by side (vs, before and after, us and them). explainer_or_infographic = steps, icons, benefit lists or a labelled diagram are the main element (the product may be small). typographic_offer = a big price, percent, bundle or sale line dominates and the product is small or absent. multi_product_collage = several products or flavours shown together as a range, no single hero. ugc_or_creator_photo = a casual photo or video frame of a real person talking, holding or using the product, shot like a phone video or selfie (a creator talking to camera is this). lifestyle_scene = a styled, professional scene (people, place, moment) where the product is secondary or in use. product_hero = the pack or product is the clear subject on a plain or styled background, even with a headline, badges, a price tag or a glass of the drink beside it. other = only if nothing above fits. If unsure between product_hero and anything else, choose product_hero unless the special feature (screen, quote, joke, comparison, steps, big offer line, range, person) is clearly the main element.
hook (the main persuasion move of headline plus image): benefit = what you get; curiosity = makes you want to find out; offer_price = the price or deal is the hook; social_proof = customer count, rating or reviews; problem_pain = names a pain; how_to_demo = shows how it works; nostalgia_home = home, mother, childhood, ghar, naani; identity_status = who you are or belonging; scarcity_urgency = limited, ending, running low; authority = doctor, expert or certification; none.
offer: what discount or deal is visible in the image or text (none if nothing). product_visibility: how large the product or pack is in the picture. people: none, hands_only, one_person, two_plus. setting: where the scene is. text_amount: none, little (under 8 words), medium, heavy (over 20 words). headline_language: the language of the main headline text (hinglish = Hindi in Roman letters).
headline_text: the main headline exactly as printed in the image (empty string if none). palette: the 2 or 3 dominant colours in plain words. claims: every kind of promise made in image or text. has_price, has_cta_button, has_social_proof: true or false.
seen: FIRST describe in at most 25 words what the picture actually shows (main subject, people, any text), then classify from that description. devices: list EVERY one of the listed visual devices that is visibly present in the picture (what you can see, not what it implies; use none only if no listed device is present): chat_bubbles = WhatsApp or iMessage style bubbles; notes_or_list_app = a notes or to-do list screen; search_box = a search bar; receipt_or_ledger = a receipt, bill, balance sheet or spreadsheet; weather_or_app_widget = a weather card or app widget; handwritten_or_sticky_note; letter_board_or_signage; crossed_out_text; checklist_ticks = tick marks or a list of ticked points; before_after_split = a vs or split-screen comparison; review_stars_or_quote = stars or a customer quote; customer_count_claim = '10,000+ customers' type text; price_sticker_or_burst = a price or starburst sticker; free_gift_badge; discount_badge = a percent-off badge; urgency_label = valid till tonight, running low, limited time; humour_wordplay_or_spoof = a joke, spoof or wordplay; creator_or_celebrity_face = a real person's face looking at the camera; mascot_or_animation; hand_holding_product; pour_or_splash = liquid pouring or splashing. idea: the concept in at most 12 plain words. device: what is visually unusual or the attention device, at most 12 words, or "none"."""


def schema():
    props = {'seen': {'type': 'string'}}
    props.update({k: {'type': 'string', 'enum': v} for k, v in ENUMS.items()})
    props.update({'headline_text': {'type': 'string'}, 'palette': {'type': 'string'}, 'idea': {'type': 'string'}, 'device': {'type': 'string'},
                  'claims': {'type': 'array', 'items': {'type': 'string', 'enum': CLAIMS}},
                  'devices': {'type': 'array', 'items': {'type': 'string', 'enum': DEVICES}},
                  'has_price': {'type': 'boolean'}, 'has_cta_button': {'type': 'boolean'}, 'has_social_proof': {'type': 'boolean'}})
    return {'type': 'object', 'properties': props, 'required': list(props), 'additionalProperties': False}


def load_index(p):
    return [r for r in json.load(open(p, encoding='utf-8')) if r.get('file') and os.path.exists(r['file'])]


def b64_image(fp, side=1024):
    from PIL import Image
    im = Image.open(fp).convert('RGB')
    im.thumbnail((side, side))
    buf = io.BytesIO()
    im.save(buf, 'JPEG', quality=85)
    return base64.b64encode(buf.getvalue()).decode()


def cmd_code(a):
    rows = load_index(a.index)
    if a.limit:
        rows = rows[:a.limit]
    done = {}
    if os.path.exists(a.out):
        done = {(r['brand'], str(r['ad'])): r for r in json.load(open(a.out, encoding='utf-8'))}
    todo = [r for r in rows if (r['brand'], str(r['ad'])) not in done]
    print('ads with an image: %d | already coded: %d | to code now: %d' % (len(rows), len(done), len(todo)))
    key = getenv('OPENAI_API_KEY')
    if not key:
        sys.exit('OPENAI_API_KEY not set')
    hdr = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'}
    sc = schema()
    lock = threading.Lock()
    tot = {'in': 0, 'out': 0, 'fail': 0}

    def one(r):
        ctx = 'Brand: %s (%s). Image type: %s. Days running: %s.\nAd title: %s\nAd text: %s\nButton: %s' % (
            r['brand'], r.get('industry'), 'video thumbnail' if r.get('kind') == 'video' else 'static image', r.get('age'), r.get('title') or '', r.get('body') or '', r.get('cta') or '')
        body = json.dumps({'model': a.model, 'messages': [
            {'role': 'system', 'content': RULES % a.about},
            {'role': 'user', 'content': [{'type': 'text', 'text': ctx},
                                         {'type': 'image_url', 'image_url': {'url': 'data:image/jpeg;base64,' + b64_image(r['file']), 'detail': 'high'}}]}],
            'response_format': {'type': 'json_schema', 'json_schema': {'name': 'ad', 'strict': True, 'schema': sc}},
            'reasoning_effort': a.effort, 'max_completion_tokens': 6000}).encode('utf-8')
        last = None
        for t in range(6):
            req = urllib.request.Request('https://api.openai.com/v1/chat/completions', data=body, headers=hdr, method='POST')
            try:
                with urllib.request.urlopen(req, timeout=180) as resp:
                    d = json.loads(resp.read().decode('utf-8'))
                out = json.loads(d['choices'][0]['message']['content'])
                u = d.get('usage', {})
                out.update({'brand': r['brand'], 'ad': r['ad'], 'n': r.get('n'), 'kind': r.get('kind'), 'age': r.get('age'), 'role': r.get('role'),
                            '_in': u.get('prompt_tokens', 0), '_out': u.get('completion_tokens', 0)})
                return out
            except urllib.error.HTTPError as e:
                last = 'HTTP %s %s' % (e.code, e.read().decode('utf-8', 'ignore')[:160])
                if e.code in (429, 500, 502, 503, 504):
                    time.sleep(2 + 3 * t)
                    continue
                break
            except Exception as e:
                last = str(e)[:160]
                time.sleep(2 + 3 * t)
        with lock:
            tot['fail'] += 1
        print('FAILED', r['brand'], r['ad'], last)
        return None

    t0 = time.time()
    with ThreadPoolExecutor(a.workers) as ex:
        for i, out in enumerate(ex.map(one, todo), 1):
            if out:
                with lock:
                    done[(out['brand'], str(out['ad']))] = out
                    tot['in'] += out['_in']
                    tot['out'] += out['_out']
            if i % 25 == 0:
                json.dump(list(done.values()), open(a.out, 'w', encoding='utf-8'), ensure_ascii=False)
                print('coded %d of %d (%.0fs)' % (i, len(todo), time.time() - t0))
    json.dump(list(done.values()), open(a.out, 'w', encoding='utf-8'), ensure_ascii=False)
    pin, pout = {'gpt-5-mini': (0.25, 2.0), 'gpt-5': (1.25, 10.0)}.get(a.model, (1.25, 10.0))   # $ per M tokens, assumed
    print('done: %d coded, %d failed | tokens in %d out %d | about $%.2f (assumed prices for %s)' % (len(done), tot['fail'], tot['in'], tot['out'], tot['in'] * pin * 1e-6 + tot['out'] * pout * 1e-6, a.model))


def norm(s):
    import re
    return re.sub('[^a-z0-9]+', '', (s or '').lower())


def prep(coded, exclude='', dedupe=False):
    """Drop brands that do not belong (restaurants, other categories) and, with dedupe, keep one record per brand + headline (the longest running);
    `copies` says how many ads share it (many copies = a brand scaling or testing one creative)."""
    ex = {x.strip().lower() for x in exclude.split(',') if x.strip()}
    rows = [c for c in coded if c['brand'].lower() not in ex]
    if not dedupe:
        return rows
    groups = {}
    for c in sorted(rows, key=lambda c: -(c.get('age') or 0)):
        key = (c['brand'], norm(c['headline_text']) or norm(c['idea']))
        if key in groups:
            groups[key]['copies'] = groups[key].get('copies', 1) + 1
        else:
            c['copies'] = 1
            groups[key] = c
    return list(groups.values())


def pct(n, d):
    return '%d (%d%%)' % (n, round(100 * n / d)) if d else '0'


def cmd_count(a):
    raw = json.load(open(a.coded, encoding='utf-8'))
    coded = prep(raw, a.exclude, a.dedupe)
    N = len(coded)
    old = [c for c in coded if (c.get('age') or 0) >= 60]
    L = ['# Competitor creative counts (vision-coded; audit by eye before quoting)', '',
         'Ads coded: %d (excluded or merged: %d; dedupe %s). Of these: static %d, video thumbnails %d, from %d brands. Running 60 days or more: %d. Run length is only a survival proxy: IN commercial ads have no spend or impressions.' % (
             N, len(raw) - N, 'on' if a.dedupe else 'off', sum(c['kind'] == 'static' for c in coded), sum(c['kind'] == 'video' for c in coded), len(set(c['brand'] for c in coded)), len(old)), '']
    for f in ENUMS:
        cnt = collections.Counter(c[f] for c in coded)
        co = collections.Counter(c[f] for c in old)
        L += ['## ' + f, '', '| value | all ads | share | running 60d+ |', '|---|---|---|---|']
        for v, n in cnt.most_common():
            L.append('| %s | %d | %d%% | %d |' % (v, n, round(100 * n / N), co.get(v, 0)))
        L.append('')
    cc = collections.Counter(COARSE[c['format']] for c in coded)
    co2 = collections.Counter(COARSE[c['format']] for c in old)
    cs = collections.Counter(COARSE[c['format']] for c in coded if c['kind'] == 'static')
    L += ['## format (6 coarse groups: quote these)', '', '| group | all | share | statics only | running 60d+ |', '|---|---|---|---|---|']
    for v, n in cc.most_common():
        L.append('| %s | %d | %d%% | %d | %d |' % (v, n, round(100 * n / N), cs.get(v, 0), co2.get(v, 0)))
    L.append('')
    dv = collections.Counter(x for c in coded for x in c.get('devices', []))
    dvo = collections.Counter(x for c in old for x in c.get('devices', []))
    dvn = collections.Counter(x for c in coded if (c.get('age') or 0) < 30 for x in c.get('devices', []))
    L += ['## visual devices (an ad can have several; objective, so quote these)', '', '| device | ads | share | under 30 days | 60 days or more |', '|---|---|---|---|---|']
    for k, n in dv.most_common():
        L.append('| %s | %d | %d%% | %d | %d |' % (k, n, round(100 * n / N), dvn.get(k, 0), dvo.get(k, 0)))
    L.append('')
    cl = collections.Counter(x for c in coded for x in c['claims'])
    L += ['## claims (an ad can make several)', '', '| claim | ads | share |', '|---|---|---|'] + ['| %s | %d | %d%% |' % (k, n, round(100 * n / N)) for k, n in cl.most_common()] + ['']
    L += ['## yes or no fields', '', '| field | ads | share |', '|---|---|---|']
    for f in ('has_price', 'has_cta_button', 'has_social_proof'):
        n = sum(1 for c in coded if c[f])
        L.append('| %s | %d | %d%% |' % (f, n, round(100 * n / N)))
    L += ['', '## palette words (top 15)', '']
    pw = collections.Counter(w.strip().lower() for c in coded for w in c['palette'].replace(' and ', ',').split(',') if w.strip())
    L.append(', '.join('%s %d' % (k, n) for k, n in pw.most_common(15)))
    L += ['', '## format by age of the ad (new tests vs survivors)', '', '| format | under 30 days | 30 to 59 days | 60 days or more |', '|---|---|---|---|']
    for v in ENUMS['format']:
        cs = [c for c in coded if c['format'] == v]
        if cs:
            L.append('| %s | %d | %d | %d |' % (v, sum((c.get('age') or 0) < 30 for c in cs), sum(30 <= (c.get('age') or 0) < 60 for c in cs), sum((c.get('age') or 0) >= 60 for c in cs)))
    rep = sorted([c for c in coded if c.get('copies', 1) >= 2], key=lambda c: -c['copies'])
    if rep:
        L += ['', '## creatives with several copies (a brand scaling or testing one idea)', '']
        for c in rep[:25]:
            L.append('- %s: %d copies, %sd, %s, %s | %s' % (c['brand'], c['copies'], c['age'], c['format'], c['hook'], c['idea']))
    L += ['', '## per brand (format mix, running 60d+)', '', '| brand | role | ads | formats | 60d+ |', '|---|---|---|---|---|']
    by = collections.defaultdict(list)
    for c in coded:
        by[c['brand']].append(c)
    for b, cs in sorted(by.items(), key=lambda x: -len(x[1])):
        fm = collections.Counter(c['format'] for c in cs).most_common(3)
        L.append('| %s | %s | %d | %s | %d |' % (b, cs[0].get('role'), len(cs), ', '.join('%s %d' % x for x in fm), sum((c.get('age') or 0) >= 60 for c in cs)))
    L += ['', '## ideas and devices of the ads running 60 days or more (read these)', '']
    for c in sorted(old, key=lambda c: -(c.get('age') or 0)):
        L.append('- %s #%s (%sd, %s, %s): %s | device: %s | headline: %s' % (c['brand'], c['n'], c['age'], c['format'], c['hook'], c['idea'], c['device'], c['headline_text'][:80]))
    open(a.report, 'w', encoding='utf-8').write('\n'.join(L))
    print('\n'.join(L[:60]))
    print('... full report:', a.report)


def sheet_of(picks, out, title):
    from PIL import Image, ImageDraw, ImageFont
    f_big = ImageFont.truetype('arialbd.ttf', 34)
    f_sm = ImageFont.truetype('arial.ttf', 18)
    cols, W, H = 5, 300, 300
    nrows = (len(picks) + cols - 1) // cols
    sh = Image.new('RGB', (cols * W, nrows * (H + 26) + 40), 'white')
    dr = ImageDraw.Draw(sh)
    dr.text((8, 8), title, fill='black', font=f_sm)
    for k, (n, r, lab) in enumerate(picks):
        im = Image.open(r['file']).convert('RGB')
        im.thumbnail((W - 6, H - 6))
        x0, y0 = (k % cols) * W, 40 + (k // cols) * (H + 26)
        sh.paste(im, (x0 + 3, y0 + 3))
        dr.rectangle((x0 + 3, y0 + 3, x0 + 56, y0 + 40), fill='orange' if r.get('kind') == 'video' else 'red')
        dr.text((x0 + 8, y0 + 4), str(n), fill='white', font=f_big)
        dr.text((x0 + 3, y0 + H + 2), lab, fill='black', font=f_sm)
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sh.save(out, quality=85)


def cmd_sheet(a):
    idx = {(r['brand'], str(r['ad'])): r for r in load_index(a.index)}
    coded = prep(json.load(open(a.coded, encoding='utf-8')), a.exclude, a.dedupe)
    vals = [v.strip() for v in a.value.split(',') if v.strip()]
    def has(c):
        f = c.get(a.field)
        return any(v in f for v in vals) if isinstance(f, list) else f in vals
    hit = [c for c in coded if has(c) and (c.get('age') or 0) >= a.min_age and (not a.kind or c.get('kind') == a.kind)]
    hit.sort(key=lambda c: -(c.get('age') or 0))
    hit = hit[:a.max]
    picks = [(i + 1, idx[(c['brand'], str(c['ad']))], '%s %sd' % (c['brand'][:16], c['age'])) for i, c in enumerate(hit) if (c['brand'], str(c['ad'])) in idx]
    sheet_of(picks, a.out, '%s = %s (%d ads, longest running first)' % (a.field, a.value, len(picks)))
    json.dump([{'n': n, 'brand': r['brand'], 'ad': r['ad'], 'age': r['age'], 'title': r.get('title'), 'body': r.get('body')} for n, r, _ in picks],
              open(os.path.splitext(a.out)[0] + '.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(len(picks), 'ads ->', a.out)


def cmd_audit(a):
    idx = {(r['brand'], str(r['ad'])): r for r in load_index(a.index)}
    coded = json.load(open(a.coded, encoding='utf-8'))
    random.Random(7).shuffle(coded)
    pick = [c for c in coded if (c['brand'], str(c['ad'])) in idx][:a.size]
    os.makedirs(a.out, exist_ok=True)
    for s in range(0, len(pick), 20):
        chunk = [(s + i + 1, idx[(c['brand'], str(c['ad']))], '#%d' % (s + i + 1)) for i, c in enumerate(pick[s:s + 20])]
        sheet_of(chunk, os.path.join(a.out, 'audit_sheet_%d.jpg' % (s // 20 + 1)), 'AUDIT sheet %d: label format and hook by eye, then compare with audit_key.json' % (s // 20 + 1))
    json.dump([{'n': i + 1, 'brand': c['brand'], 'ad': c['ad'], 'format': c['format'], 'hook': c['hook'], 'offer': c['offer'], 'people': c['people'], 'setting': c['setting']}
               for i, c in enumerate(pick)], open(os.path.join(a.out, 'audit_key.json'), 'w', encoding='utf-8'), indent=1)
    print(len(pick), 'ads in', (len(pick) + 19) // 20, 'sheets ->', a.out)


if __name__ == '__main__':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('code', 'count', 'sheet', 'audit'):
        p = sub.add_parser(name)
        p.add_argument('--index', required=True)
        if name == 'code':
            p.add_argument('--out', required=True); p.add_argument('--about', required=True)
            p.add_argument('--workers', type=int, default=8); p.add_argument('--limit', type=int, default=0)
            p.add_argument('--model', default=MODEL); p.add_argument('--effort', default='low')
        if name in ('count', 'sheet', 'audit'):
            p.add_argument('--coded', required=True)
        if name in ('count', 'sheet'):
            p.add_argument('--exclude', default=''); p.add_argument('--dedupe', action='store_true')
        if name == 'count':
            p.add_argument('--report', required=True)
        if name == 'sheet':
            p.add_argument('--field', required=True); p.add_argument('--value', required=True); p.add_argument('--out', required=True); p.add_argument('--max', type=int, default=20)
            p.add_argument('--min-age', dest='min_age', type=int, default=0); p.add_argument('--kind', default='')
        if name == 'audit':
            p.add_argument('--out', required=True); p.add_argument('--size', type=int, default=60)
    a = ap.parse_args()
    {'code': cmd_code, 'count': cmd_count, 'sheet': cmd_sheet, 'audit': cmd_audit}[a.cmd](a)
