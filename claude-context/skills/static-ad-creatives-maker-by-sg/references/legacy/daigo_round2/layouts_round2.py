"""Daigo round 2 layouts (2026-10-10). Code places the real pack crop, the logo, stickers and (typed arm) every word, from round2\\copy_r2.json.
  python layouts_round2.py render [ID ...]   -> layouts\\<ID>.json and img\\<ID>.png
Colours only from the brand kit (tokens like $navy); raw html uses tok()."""
import json, os, re, sys, subprocess, random
sys.path.insert(0, 'C:/cca/daigo/round2')
from build_round2 import ROOT, R2, SK, KITP, PAL, PACK, LB, LW, FONTS, SIZE

COPY2 = json.load(open(R2 + '/copy_r2.json', encoding='utf-8'))


def tok(n):
    if n not in PAL:
        raise SystemExit('colour not in the brand kit: ' + n)
    return PAL[n]


def scene(i):
    return R2 + '/img/scene_%s.png' % i


def pack(x, y, w, rot=0, over=False):
    return {'src': PACK, 'x': x, 'y': y, 'w': w, 'rotate': rot, 'shadow': True, 'over': over}


def glow(cx, cy, size, a=0.45, col='255,255,255'):
    px = size * 10.8
    return {'html': "<div style=\"position:absolute;left:%s%%;top:%s%%;width:%dpx;height:%dpx;margin:-%dpx 0 0 -%dpx;background:radial-gradient(closest-side, rgba(%s,%s), rgba(%s,0));\"></div>" % (cx, cy, px, px, px / 2, px / 2, col, a, col)}


def logo(x, y, w, kind='blue'):
    return {'src': LB if kind == 'blue' else LW, 'x': x, 'y': y, 'w': w}


def scrim(h_pct, top=True, a=0.7, col='12,20,46'):
    d = 'to bottom' if top else 'to top'
    y = 0 if top else 100 - h_pct
    return {'text': '', 'x': 0, 'y': y, 'w': 100, 'size': 1, 'css': 'height:%s%%;background:linear-gradient(%s, rgba(%s,%s), rgba(%s,0));' % (h_pct, d, col, a, col)}


def base(**kw):
    L = {'kit': KITP, 'size': SIZE, 'fonts': FONTS, 'images': [], 'elements': [], 'stacks': []}
    L.update(kw)
    return L


def outline(x, y, w, rot=0, m=3.5, ext=24):
    """a die-cut white outline behind the pack (sticker look): the pack separates from any photo (QA check 12) without a haze over the picture.
    Same centre and rotation as the pack; it runs past the bottom edge because the pack crop bleeds off the canvas."""
    h = w * 0.858
    top = y - m
    height = h + 2 * m + ext
    oy = (m + h / 2) / height * 100
    return {'html': ('<div style="position:absolute;left:%.2f%%;top:%.2f%%;width:%.2f%%;height:%.2f%%;background:#FFFFFF;border-radius:%.2f%%;'
                     'box-shadow:0 10px 26px rgba(0,0,0,.30);transform:rotate(%sdeg);transform-origin:50%% %.1f%%"></div>') % (x - m, top, w + 2 * m, height, 3.4, rot, oy)}


def hl(c, color='$jaljira_yellow', which=None):
    """headline html: lines joined with <br>; the line(s) listed in c['em'] (or `which`) get the accent colour"""
    em = c.get('em', []) if which is None else which
    out = []
    for k, line in enumerate(c['h']):
        out.append("<span style='color:%s'>%s</span>" % (color, line) if k in em else line)
    return '<br>'.join(out)


def sachet_svg(rot=0, uid=0):
    teeth = 10
    top = 'M4 9 ' + ' '.join('L%.1f 3 L%.1f 9' % (4 + 6.2 * i + 3.1, 4 + 6.2 * (i + 1)) for i in range(teeth))
    bot = ' '.join('L%.1f 107 L%.1f 101' % (66 - 6.2 * i - 3.1, 66 - 6.2 * (i + 1)) for i in range(teeth))
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 70 110' style='width:100%%;height:auto;display:block;transform:rotate(%sdeg);filter:drop-shadow(0 3px 3px rgba(0,0,0,.28))'>"
            "<defs><linearGradient id='g%d' x1='0' x2='1'><stop offset='0' stop-color='#BFC6CE'/><stop offset='.42' stop-color='#F3F5F7'/><stop offset='1' stop-color='#AEB6BF'/></linearGradient></defs>"
            "<path d='%s L66 101 %s L4 9 Z' fill='url(#g%d)' stroke='#98A2AC' stroke-width='.8'/>"
            "<path d='M10 22 V92 M60 22 V92' stroke='#FFFFFF' stroke-opacity='.55' stroke-width='1.2'/></svg>") % (rot, uid, top, bot, uid)


def sachet_grid(n, cols, x, y, w, gap_pct=3.0, seed=3):
    rnd = random.Random(seed)
    cells = ''.join("<div>%s</div>" % sachet_svg(rnd.choice([-3, -2, -1, 0, 1, 2, 3]), i) for i in range(n))
    return {'text': "<div style='display:grid;grid-template-columns:repeat(%d,1fr);gap:%s%% %s%%'>%s</div>" % (cols, gap_pct, gap_pct * 0.9, cells), 'x': x, 'y': y, 'w': w, 'size': 1}


def burst(lines, x, y, size_pct, rot=-8, bg='jaljira_yellow', fg='navy'):
    """round sticker: lines = [(text, relative size)], first line biggest"""
    px = size_pct * 10.8
    rows = ''.join("<div style=\"font:800 %dpx 'Baloo 2';color:%s;line-height:.92;letter-spacing:.01em\">%s</div>" % (px * s, tok(fg), t) for t, s in lines)
    return {'text': "<div style=\"width:%dpx;height:%dpx;border-radius:50%%;background:%s;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;"
                    "box-shadow:0 10px 20px rgba(0,0,0,.32);transform:rotate(%sdeg);border:%dpx solid %s\">%s</div>" % (px, px, tok(bg), rot, px * 0.025, tok('white'), rows),
            'x': x, 'y': y, 'w': size_pct, 'size': 1}


def strip(items, y, h=11, bg='navy', fg='white'):
    """a full-width price strip with N items separated by thin rules"""
    cells = ''.join("<div style=\"flex:1;text-align:center;font:800 %dpx 'Baloo 2';color:%s;%s\">%s</div>" % (h * 10.8 * 0.42, tok(fg), 'border-left:3px solid rgba(255,255,255,.35);' if k else '', t) for k, t in enumerate(items))
    return {'text': "<div style=\"display:flex;align-items:center;height:%dpx;background:%s\">%s</div>" % (h * 10.8, tok(bg), cells), 'x': 0, 'y': y, 'w': 100, 'size': 1}


# ------------------------------------------------------------------ layouts (filled after the critic pass; see copy_r2.json)
LAYOUTS = {}


def clamp(L):
    """Edge safety (design rule: all text and logos inside the central 84%): text starts at 8% from the top, logos end by 92%."""
    for im in L.get('images', []):
        if im.get('src') in (LB, LW):
            h = im['w'] * (0.37 if im['src'] == LB else 0.356)
            if im['y'] < 50:
                im['y'] = max(im['y'], 8)
            else:
                im['y'] = round(min(im['y'], 92 - h), 2)
    for st in L.get('stacks', []):
        st['y'] = max(st['y'], 8)
    for e in L.get('elements', []):
        if e.get('text', '').strip() and e.get('size', 0) > 1.5 and e.get('y', 50) < 8:
            e['y'] = 8
    return L


def render(ids):
    ids = ids or list(LAYOUTS)
    for i in ids:
        try:
            L = clamp(LAYOUTS[i]())
        except FileNotFoundError as e:
            print(i, 'SKIP (scene missing):', e)
            continue
        lp = R2 + '/layouts/%s.json' % i
        json.dump(L, open(lp, 'w', encoding='utf-8'), indent=1)
        r = subprocess.run(['python', SK + '/render_ad.py', lp, R2 + '/img/%s.png' % i], capture_output=True, text=True)
        print(i, (r.stdout + r.stderr).strip()[-160:])


if __name__ == '__main__':
    exec(open(R2 + '/layouts_defs.py', encoding='utf-8').read())
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    {'render': lambda: render(sys.argv[2:])}[cmd]()
