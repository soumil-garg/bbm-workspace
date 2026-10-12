"""whole_ad.py: the v3 image step (2026-10-10, the recipe Soumil loved on Daigo round 4).
The image model draws the WHOLE ad (scene, real product, product forms, headline, badges) in one pass from reference images of the real product.
Nothing is pasted on afterwards: no code text layer, no cut-out pack, no die-cut tile. Manual: references/whole-ad-recipe.md.

Run from anywhere with the full path (the skill folder is C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg), forward slashes in Git Bash:
  python <skill>/scripts/whole_ad.py validate --config <ads_config.json>
  python <skill>/scripts/whole_ad.py prompts  --config <ads_config.json> [ID ...] [--tag _v2]
  python <skill>/scripts/whole_ad.py gen      --config <ads_config.json> [ID ...] [--tag _v2] [--workers 5] [--only-missing] [--force]
  python <skill>/scripts/whole_ad.py qa       --config <ads_config.json> [--tag _v2]   (numbered QA sheets in <dir>/qa, for YOUR eyes, not for delivery)
  python <skill>/scripts/whole_ad.py status   --config <ads_config.json>

The config is JSON. Start from references/templates/ads_config.skeleton.json (blank) and read ads_config.example.json (the Daigo round 4 gold config).
Prompt = ROLE_REFS (what each reference image is) + ART (the construction brief) + concept body + NEG (the avoid list), joined by single spaces.
gen never overwrites a picture that exists (use --force, or a new --tag such as _v2); a tagged run writes its own prompt file p/<id><tag>.txt.
Cost is logged by gen_image.py to C:/cca/_ledger/openai_images.jsonl (about $0.066 per 1024x1280 picture)."""
import argparse, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.normpath(HERE + '/..').replace('\\', '/')
GEN = HERE + '/gen_image.py'
LEDGER = 'C:/cca/_ledger/openai_images.jsonl'

DEFAULT_TOP = " The first line of the headline starts at least 9% below the top edge."

# The construction brief. Only the palette (and, for dry goods, the finish words) change per brand. This paragraph is what makes the output look like a designed poster, not a pasted picture.
ART_TEMPLATE = ("Create a FINISHED professional Meta feed advertisement, 4:5 portrait, art directed like a top D2C brand poster, in the construction style of the best static ads: ONE clear focal point; "
                "a disciplined palette of at most three brand hues ({palette}) plus white and the product's own colours; the background is a designed colour field or a built studio set, not a casual snapshot; "
                "clean soft studio lighting with soft believable shadows, {finish}; three-level type hierarchy (a huge headline, one small supporting line, optional tiny badge); the typography is part of the design (it overlaps, wraps or sits behind elements where that helps) and carries one treatment such as a highlight bar, an underline swoosh or a two-colour split; "
                "the headline and the picture tell ONE story and the product takes part in that story; generous margins, all text and key objects inside the central 84% of the frame, nothing important touching an edge. "
                "Every piece of text must be spelled EXACTLY as given, letter for letter, cleanly rendered and aligned. No other text, no watermark, no fake UI.")
DEFAULT_FINISH = "specular highlights and condensation"   # a drink or anything cold; for dry goods set "finish": "specular highlights" in the config

# Generic avoid list. Presets add the items that only matter for some categories; "neg_items" in the config replaces the whole list.
DEFAULT_NEG_ITEMS = ["a pasted-on look", "flat cut-out products", "a casual phone-snapshot look", "empty unused space", "plain unbranded product forms", "stock-photo smiles", "extra logos",
                     "invented claims", "health claims", "any text that was not specified", "garbled lettering", "extra fingers",
                     "readable text on any background object (book spines, signboards, labels, screens) other than the text specified", "the logo of any real company"]
NEG_PRESETS = {'drink': ["white powder clouds, white liquid splashes or sprays", "clinking glasses", "unlabelled clear bottles"],
               'powder': ["white powder clouds"]}

# High-severity slang from the native-reader screen (references/hinglish-never-use.md). The reader agent does the real screen; this only stops the known ones.
PLACEHOLDER = re.compile(r'<[A-Za-z][^<>]{0,70}>')
NEVER = re.compile(r'\b(phaado|phaad|phaadna|hilao|hila|hilana|daalo|daal do)\b', re.I)
BAD_CHARS = re.compile('[\u2014\u2013*\u2018\u2019\u201c\u201d]')          # em dash, en dash, asterisk, curly quotes
MONEY = re.compile(r'(\bRs\.? ?\d|\u20b9|\$\s?\d|\d\s?%|\bfree\b|\boff\b|\bbuy \d)', re.I)
LANGS_OK = {'EN', 'HG', 'MIX'}


def expand(p):
    return p.replace('{SKILL}', SKILL)


def load(path):
    cfg = json.load(open(path, encoding='utf-8'))
    cfg['_dir'] = expand(cfg.get('dir') or os.path.dirname(os.path.abspath(path)))
    for r in cfg.get('refs', []):
        if 'path' in r:
            r['path'] = expand(r['path'])
    for c in cfg.get('concepts', []):
        for r in c.get('extra_refs', []):
            r['path'] = expand(r['path'])
    for it in cfg.get('delivery', []):
        if it.get('carry'):
            it['carry'] = expand(it['carry'])
    return cfg


def ensure_dirs(cfg):
    for d in ('p', 'out'):
        os.makedirs(cfg['_dir'] + '/' + d, exist_ok=True)


def role_refs(cfg, concept):
    refs = list(cfg['refs']) + list(concept.get('extra_refs', []))
    first = 'REFERENCE IMAGES: ' + '; '.join('image %d is %s' % (k + 1, r['role']) for k, r in enumerate(refs)) + '.'
    return ' '.join([first] + cfg.get('ref_rules', []))


def art(cfg):
    return ART_TEMPLATE.format(palette=cfg['palette'], finish=cfg.get('finish', DEFAULT_FINISH))


def neg(cfg):
    if cfg.get('neg_items'):
        items = cfg['neg_items']
    else:
        items = list(DEFAULT_NEG_ITEMS)
        for p in cfg.get('neg_preset', []):
            items += NEG_PRESETS[p]
        items += cfg.get('neg_extra', [])
    return 'Avoid: ' + ', '.join(items) + '.'


def body(cfg, c):
    b = c['body']
    sub = {'{TOP}': cfg.get('top_rule', DEFAULT_TOP), '{SMALL}': cfg.get('small_line', '')}
    sub.update({'{%s}' % k: v for k, v in cfg.get('vars', {}).items()})
    for k, v in sub.items():
        b = b.replace(k, v)
    return b


def assemble(cfg, c):
    return ' '.join([role_refs(cfg, c), art(cfg), body(cfg, c), neg(cfg)])


def pick(cfg, ids):
    cs = {c['id']: c for c in cfg['concepts']}
    if not ids:
        return list(cs.values())
    miss = [i for i in ids if i not in cs]
    if miss:
        sys.exit('unknown concept ids: %s' % miss)
    return [cs[i] for i in ids]


def norm(s):
    return re.sub(r'[^a-z0-9]+', ' ', (s or '').lower()).strip()


def cmd_validate(cfg):
    errs, warns = [], []
    brand = cfg.get('brand', '')
    blob = json.dumps({k: v for k, v in cfg.items() if k not in ('_about', 'concepts', 'delivery')}, ensure_ascii=False)
    for c in cfg.get('concepts', []):
        blob += ' ' + c.get('body', '') + ' ' + c.get('line', '') + ' ' + ' '.join(c.get('texts', []))
    ph = sorted(set(PLACEHOLDER.findall(blob)))
    if ph:
        errs.append('unfilled placeholders (the config is still the skeleton): %s' % ph[:8])
    refs = cfg.get('refs', [])
    if not refs:
        errs.append('"refs" is empty: without a reference image the model invents the pack (the failure that made round 2 look wrong)')
    for r in refs:
        if not r.get('role'):
            errs.append('a reference has no "role" sentence: %s' % r.get('path'))
        if not os.path.exists(r.get('path', '')):
            errs.append('reference image missing: %s' % r.get('path'))
    if len(refs) > 4:
        warns.append('%d reference images; fidelity drops past about 3 or 4 (keep the pack and one reference per form)' % len(refs))
    if not cfg.get('ref_rules'):
        warns.append('no "ref_rules" (fidelity, form rule, no-extras rule, integration rule: recipe section 4)')
    if not cfg.get('palette'):
        errs.append('no "palette"')
    if brand.lower() != 'daigo':
        for k in ('dir', 'dest'):
            if 'daigo' in (cfg.get(k) or '').lower():
                errs.append('"%s" still points at the Daigo folders: %s' % (k, cfg.get(k)))
    pats = []
    for pat in cfg.get('banned_phrases', []):
        if re.search('[\x00-\x1f]', pat):
            errs.append('banned_phrases entry contains a control character (a single backslash in JSON turns \\b into a backspace; write \\\\b): %r' % pat)
            continue
        try:
            pats.append(re.compile(pat, re.I))
        except re.error as e:
            errs.append('banned_phrases entry is not a valid regex: %r (%s)' % (pat, e))
    seen, nums = set(), set()
    langs = {}
    for c in cfg['concepts']:
        i = c['id']
        if i in seen:
            errs.append('duplicate id %s' % i)
        seen.add(i)
        if c.get('num') in nums:
            errs.append('duplicate number %s' % c.get('num'))
        nums.add(c.get('num'))
        typ = c.get('type', 'poster')
        if typ not in ('poster', 'native'):
            errs.append('%s: type must be poster or native, got %r' % (i, typ))
        p = assemble(cfg, c)
        texts = c.get('texts', [])
        for t in texts:
            if t not in p:
                errs.append('%s: on-image text not found in the prompt, exact string: %r' % (i, t))
            if BAD_CHARS.search(t):
                errs.append('%s: on-image text contains an em dash, en dash, asterisk or curly quote (published-content style): %r' % (i, t))
        if not texts:
            warns.append('%s: no "texts" list (list every exact on-image string so QA can tick them off)' % i)
        if typ == 'poster':
            if 'HEADLINE' not in p:
                errs.append('%s: poster without a HEADLINE block' % i)
            if cfg.get('top_rule', DEFAULT_TOP).strip() not in p:
                errs.append('%s: poster without the top-margin rule ({TOP})' % i)
        if BAD_CHARS.search(c['body']):
            warns.append('%s: the concept body contains an em dash, asterisk or curly quote' % i)
        for t in texts + [c.get('line', '')]:
            if NEVER.search(t or ''):
                errs.append('%s: contains a banned slang word (references/hinglish-never-use.md): %r' % (i, t))
        for rx in pats:
            for t in texts:
                if rx.search(t):
                    errs.append('%s: on-image text hits the claim ban %r: %r' % (i, rx.pattern, t))
        line = c.get('line', '')
        if line and texts:
            joined = norm(' '.join(texts))
            for part in re.split(r'\s/\s|(?<=[.?!])\s+', line):
                if norm(part) and norm(part) not in joined:
                    warns.append('%s: part of the approved line is not in texts: %r' % (i, part))
        if typ == 'poster':
            for rt in cfg.get('required_texts', []):
                if rt not in texts and not c.get('skip_required'):
                    errs.append('%s: required text missing from texts (client-mandated on every ad): %r' % (i, rt))
        if any(MONEY.search(t) for t in texts) and not cfg.get('offers_verified'):
            warns.append('%s: an offer or price is on the picture but "offers_verified" is empty (verify on the live site today, log the page and the date)' % i)
        if brand.lower() != 'daigo' and re.search(r'daigo|chaas', p + ' ' + ' '.join(texts), re.I):
            errs.append('%s: Daigo content leaked into a %s prompt (daigo / chaas)' % (i, brand))
        lang = c.get('lang')
        if not lang:
            warns.append('%s: no "lang" (EN, HG or MIX)' % i)
        else:
            langs[lang] = langs.get(lang, 0) + 1
            if lang not in LANGS_OK and lang not in cfg.get('languages', []):
                warns.append('%s: lang %r is not EN, HG or MIX and not listed in "languages"' % (i, lang))
        if len(p) > 4800:
            warns.append('%s: prompt is %d characters; the loved ones were 3,400 to 4,400' % (i, len(p)))
    print('concepts:', len(cfg['concepts']), '| language mix:', langs)
    for w in warns:
        print('WARN', w)
    for e in errs:
        print('ERROR', e)
    print('validate:', 'FAILED' if errs else 'ok', '| NOTE: validate checks structure and known bans only; the slang screen (native reader), the claim register and QA at zoom are separate and still required')
    return 1 if errs else 0


def cmd_prompts(cfg, ids, tag=''):
    ensure_dirs(cfg)
    cs = pick(cfg, ids)
    for c in cs:
        open(cfg['_dir'] + '/p/%s%s.txt' % (c['id'], tag), 'w', encoding='utf-8').write(assemble(cfg, c))
    print('prompts written:', [c['id'] + tag for c in cs])


def cmd_gen(cfg, ids, tag, workers, only_missing, force):
    ensure_dirs(cfg)
    cs = pick(cfg, ids)
    keep = []
    for c in cs:
        out = cfg['_dir'] + '/out/%s%s.png' % (c['id'], tag)
        if os.path.exists(out) and not force:
            print('SKIP %s%s: a picture already exists (use --force to overwrite, or a new --tag such as _v2)' % (c['id'], tag))
            continue
        keep.append(c)
    cs = keep
    if not cs:
        print('nothing to generate')
        return
    cmd_prompts(cfg, [c['id'] for c in cs], tag)

    def one(c):
        refs = [r['path'] for r in cfg['refs']] + [r['path'] for r in c.get('extra_refs', [])]
        cmd = [sys.executable, GEN, '--prompt-file', cfg['_dir'] + '/p/%s%s.txt' % (c['id'], tag), '--out', cfg['_dir'] + '/out/%s%s.png' % (c['id'], tag),
               '--size', c.get('size', cfg.get('size', '1024x1280')), '--quality', cfg.get('quality', 'high'),
               '--tag', '%s_%s%s' % (cfg.get('tag_prefix', 'ads'), c['id'], tag), '--model', cfg.get('model', 'gpt-image-2.5-sunburst')]
        for r in refs:
            cmd += ['--ref', r]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return c['id'], (r.stdout + r.stderr).strip()[-170:]
    with ThreadPoolExecutor(workers) as ex:
        for i, msg in ex.map(one, cs):
            print(i, '->', msg)


def cmd_qa(cfg, tag=''):
    from PIL import Image, ImageDraw, ImageFont
    ensure_dirs(cfg)
    os.makedirs(cfg['_dir'] + '/qa', exist_ok=True)
    cs = [c for c in cfg['concepts'] if os.path.exists(cfg['_dir'] + '/out/%s%s.png' % (c['id'], tag))]
    W, cols, per = 620, 3, 6
    f = ImageFont.truetype('arialbd.ttf', 22)
    for s in range(0, len(cs), per):
        chunk = cs[s:s + per]
        H = int(W * 1.25)
        rows = (len(chunk) + cols - 1) // cols
        sheet = Image.new('RGB', (cols * W, rows * (H + 34)), 'white')
        d = ImageDraw.Draw(sheet)
        for k, c in enumerate(chunk):
            im = Image.open(cfg['_dir'] + '/out/%s%s.png' % (c['id'], tag)).convert('RGB')
            im.thumbnail((W - 6, H - 6))
            x, y = (k % cols) * W, (k // cols) * (H + 34)
            d.text((x + 8, y + 5), '%s %s%s' % (c.get('num', ''), c['id'], tag), fill='black', font=f)
            sheet.paste(im, (x + 3, y + 34))
        out = cfg['_dir'] + '/qa/qa%s_%d.jpg' % (tag, s // per + 1)
        sheet.save(out, quality=90)
        print(out, sheet.size)


def cmd_status(cfg):
    spent = {}
    if os.path.exists(LEDGER):
        for line in open(LEDGER, encoding='utf-8'):
            r = json.loads(line)
            if str(r.get('tag', '')).startswith(cfg.get('tag_prefix', 'ads') + '_'):
                spent[r['tag']] = spent.get(r['tag'], 0) + r['usd']
    have = [c['id'] for c in cfg['concepts'] if os.path.exists(cfg['_dir'] + '/out/%s.png' % c['id'])]
    print('pictures made: %d of %d | ledger spend under tag prefix %s: $%.2f over %d runs' % (len(have), len(cfg['concepts']), cfg.get('tag_prefix', 'ads'), sum(spent.values()), len(spent)))
    print('missing:', [c['id'] for c in cfg['concepts'] if c['id'] not in have])


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['validate', 'prompts', 'gen', 'qa', 'status'])
    ap.add_argument('ids', nargs='*')
    ap.add_argument('--config', required=True)
    ap.add_argument('--tag', default='')
    ap.add_argument('--workers', type=int, default=5)
    ap.add_argument('--only-missing', action='store_true')
    ap.add_argument('--force', action='store_true')
    a = ap.parse_args()
    cfg = load(a.config)
    if a.cmd == 'validate':
        sys.exit(cmd_validate(cfg))
    elif a.cmd == 'prompts':
        cmd_prompts(cfg, a.ids, a.tag)
    elif a.cmd == 'gen':
        cmd_gen(cfg, a.ids, a.tag, a.workers, a.only_missing, a.force)
    elif a.cmd == 'qa':
        cmd_qa(cfg, a.tag)
    else:
        cmd_status(cfg)
