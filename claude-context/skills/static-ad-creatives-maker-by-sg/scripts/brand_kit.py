"""Brand kit: capture a brand's real colours, fonts and logo once, then keep every creative inside it.

  python brand_kit.py extract <site_url> <out_dir> [packshot1.jpg packshot2.png ...]
      Reads the live site (CSS colours with usage counts, font families, logo candidates) and the dominant colours of the
      packshots. Writes <out_dir>/brand-kit.candidates.json. LOOK at it, then write the curated <out_dir>/brand-kit.json by hand.
  python brand_kit.py check <brand-kit.json> <creative.png>
      QA check 13 (brand fit): dominant colours of the creative vs the kit. Fails when the main background colour or a large
      accent area is outside the kit and not declared as a test accent.

Three tiers (so the kit protects the brand WITHOUT making every ad look the same):
  core   = identity that never changes: logo, wordmark, product and pack accuracy, brand fonts for brand-owned text.
  flex   = the brand's extended palette: core colours plus tints and shades of them, colours that appear on the packaging or the
           site, and neighbouring colours. This is where visual variety comes from. Most designed ads should use a flex background.
  test   = colours outside the brand (e.g. lime), allowed only as a labelled test arm, at most about 25% of a round.
  Native / UGC / lifestyle-photo ads (bucket 4 and real-world scenes) are EXEMPT from the colour check: they take the colours of the
  real scene. They keep only product accuracy and the logo rules. Pass --native to check to skip the colour verdict.
Round-level variety is enforced separately by scripts/round_diversity.py (QA check 14).

brand-kit.json (curated):
{
 "brand": "Habbits", "site": "https://habbits.in",
 "colors": {                      # name -> hex. These names are usable in layout.json as "$name"
   "ink": "#111111", "paper": "#F4F1EC", "white": "#FFFFFF", "teal": "#108474"      # core
 },
 "flex": {"teal_light": "#DCEFEA", "teal_dark": "#0A5247", "cream": "#E1DAD1", "sage": "#B9C3A3", "charcoal": "#2B2B2B"},
 "roles": {"background": ["ink", "paper", "white", "teal"], "accent": ["teal"]},
 "test_accents": {"lime": "#C9F24B"},     # allowed only in a labelled test arm, approved by Soumil on <date>
 "fonts": {"heading": "Poppins", "body": "Poppins", "wordmark": "serif logo, use the logo file, never retype it",
           "display_ad": "Anton / Archivo Black are NOT brand fonts; use only if Soumil approves for ad headlines"},
 "logo_files": ["C:/cca/<brand>/ref/logo.png"],
 "voice": "one sentence",
 "source_notes": "where each colour came from (packaging photo, site CSS) and the date"
}
Rules: every background, accent and type colour comes from `colors` (or a declared test accent). A colour outside the kit is a
design decision that must be flagged to Soumil, not a default. Never invent a brand colour.
"""
import sys, re, json, os, collections, urllib.request
from PIL import Image


def get(u, binary=False):
    d = urllib.request.urlopen(urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0'}), timeout=25).read()
    return d if binary else d.decode('utf-8', 'ignore')


def hexof(c):
    return '#%02X%02X%02X' % tuple(c)


def dominant(path, k=8):
    im = Image.open(path).convert('RGB')
    im.thumbnail((200, 200))
    q = im.quantize(colors=k, method=Image.Quantize.MEDIANCUT)
    pal = q.getpalette()[:k * 3]
    cnt = collections.Counter(q.get_flattened_data() if hasattr(q, "get_flattened_data") else q.getdata())
    n = sum(cnt.values())
    return [(hexof(pal[i * 3:i * 3 + 3]), round(100 * c / n, 1)) for i, c in cnt.most_common()]


def cmd_extract(url, out, packs):
    os.makedirs(out, exist_ok=True)
    html = get(url)
    css = html
    for m in re.findall(r'href="([^"]+\.css[^"]*)"', html)[:8]:
        try:
            css += get(m if m.startswith('http') else ('https:' + m if m.startswith('//') else url.rstrip('/') + m))
        except Exception:
            pass
    colors = collections.Counter(x.upper() for x in re.findall(r'#[0-9a-fA-F]{6}\b', css))
    fonts = collections.Counter(f.strip().strip("'\"").split(',')[0].strip("'\"") for f in re.findall(r'font-family:\s*([^;}{]+)', css))
    logos = sorted(set(re.findall(r'(?:src|href|content)="([^"]*logo[^"]*\.(?:png|svg|webp|jpg)[^"]*)"', html, flags=re.I)))[:6]
    res = {'site': url, 'css_colors': colors.most_common(16), 'fonts': fonts.most_common(8), 'logo_candidates': logos,
           'packshots': {os.path.basename(p): dominant(p) for p in packs},
           'note': 'Candidates only. Curate brand-kit.json by hand: pick roles, drop theme-plugin colours, record sources.'}
    json.dump(res, open(os.path.join(out, 'brand-kit.candidates.json'), 'w'), indent=1)
    print(json.dumps(res, indent=1)[:3000])


def rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def dist(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def cmd_check(kitp, img):
    tol = float(sys.argv[sys.argv.index('--tolerance') + 1]) if '--tolerance' in sys.argv else 45.0
    advisory = '--advisory' in sys.argv
    kit = json.load(open(kitp, encoding='utf-8'))
    allowed = {n: rgb(h) for n, h in {**kit['colors'], **kit.get('flex', {})}.items()}
    native = '--native' in sys.argv
    tests = {n: rgb(h) for n, h in kit.get('test_accents', {}).items()}
    dom = dominant(img, 6)
    verdict, lines = 'PASS', []
    for h, share in dom:
        c = rgb(h)
        nk = min(allowed.items(), key=lambda kv: dist(kv[1], c))
        nt = min(tests.items(), key=lambda kv: dist(kv[1], c)) if tests else None
        if dist(nk[1], c) <= tol:
            tag = f'in kit ({nk[0]})'
        elif nt and dist(nt[1], c) <= tol:
            tag = f'TEST accent ({nt[0]}): only valid in a labelled test arm'
        else:
            tag = f'OFF KIT (nearest {nk[0]}, distance {round(dist(nk[1], c))})'
            if share >= 20:
                verdict = 'FAIL'
            elif share >= 5 and verdict == 'PASS':
                verdict = 'REVIEW'
        lines.append(f'{h} {share:>5}%  {tag}')
    if native:
        verdict = 'EXEMPT (native / real-scene ad: colours follow the scene; check product accuracy and logo only)'
    elif advisory and verdict == 'FAIL':
        verdict = 'REVIEW (advisory: a generated picture is lit by its scene, so the model never renders a kit hex exactly; look at it)'
    print(verdict)
    print('\n'.join(lines))
    print('Note: product photography (skin, wood, fruit) can be legitimately off-kit; REVIEW means look, FAIL means a background or large area is off-brand.')


if __name__ == '__main__':
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == 'extract':
        cmd_extract(a[1], a[2], a[3:])
    elif len(a) >= 3 and a[0] == 'check':
        cmd_check(a[1], a[2])
    else:
        sys.exit(__doc__)
