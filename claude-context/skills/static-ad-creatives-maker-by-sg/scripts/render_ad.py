"""EDIT TOOL ONLY since v3.0 (2026-10-10): never the first look of a brand ad (the pasted look Soumil rejected). Use it on a FINISHED picture for a price or date swap, a resize or long text.
Code text layer: put exact text on a model-drawn background with HTML/CSS, screenshot with headless Chrome.

Usage: python render_ad.py layout.json out.png

layout.json:
{
 "bg": "path/to/finished_picture.png", # the FINISHED picture you are editing (a price or date swap, a resize); v2 drew scenes with empty text zones, v3 does not
 "bg_color": "#F4F1EC",              # used when no bg image
 "size": [1080, 1080],               # output pixels
 "fonts": ["Anton", "Archivo Black"],# Google Fonts to load (needs internet; falls back to Impact/Arial Black)
 "elements": [
   {"text": "PICK ANY 3.<br>PAY FOR 2.",  # <br> for line breaks; <mark> is styled with "mark_bg"
    "x": 8, "y": 6, "w": 84,               # percent of the canvas (x, y = top-left; w = width)
    "font": "Archivo Black", "size": 11,   # size = percent of canvas HEIGHT
    "color": "#111111", "weight": 900, "align": "center", "line": 1.0, "track": -0.01,
    "mark_bg": "#C9F24B"},                 # background colour for <mark> spans
   {"text": "BUY 2 GET 1 FREE", "x": 30, "y": 86, "w": 40, "font": "Archivo Black", "size": 3.2, "color": "#111111",
    "pill": "#C9F24B", "pad": [1.2, 3], "radius": 99, "align": "center"}
 ]
}
"images": [ {"src": "C:/cca/<brand>/ref/logo_new_01.png", "x": 6, "y": 4, "w": 22} ]   # optional: a logo or a small patch over a finished picture; NEVER a cropped pack placed on a generated scene (the pasted look)
"kit": "C:/cca/<brand>/kit/brand-kit.json",   # optional: lets colours be written as "$ink", "$teal", "$lime" (test accent); unknown tokens error out
"stacks": [ {"x": 6, "y": 6, "w": 88, "items": [ {text, size, font, color, align, gap, ...}, ... ]} ]   # preferred: items flow top to bottom,
   "gap" is the space above an item in percent of height; use stacks for headline + sub line so nothing collides.
Rules: keep all text inside the central 84% of the canvas; one headline at least 3x the next text size; text comes from the
approved copy file, never retyped. In v3 the MODEL draws the text and the pack on every brand ad (scripts/whole_ad.py); use this tool only to edit a finished picture.
"""
import sys, json, os, subprocess, base64, html as H

CHROME = r'C:\Program Files\Google\Chrome\Application\chrome.exe'


def resolve_tokens(L):
    """If layout has "kit": path/to/brand-kit.json, any colour written as "$name" resolves to the kit colour
    (kit colors first, then test_accents). Unknown tokens raise, so an off-kit colour cannot slip in silently."""
    if not L.get('kit'):
        return L
    kit = json.load(open(L['kit'], encoding='utf-8'))
    pal = {**kit.get('test_accents', {}), **kit.get('flex', {}), **kit['colors']}   # v2.1: flex colours are tokens too (variety comes from flex)

    def fix(v):
        if isinstance(v, str) and v.startswith('$'):
            if v[1:] not in pal:
                raise SystemExit(f"colour token {v} is not in the brand kit ({', '.join(pal)})")
            return pal[v[1:]]
        if isinstance(v, str) and 'span style' in v:
            import re as _re
            return _re.sub(r'\$(\w+)', lambda m: pal[m.group(1)], v)
        if isinstance(v, dict):
            return {k: fix(x) for k, x in v.items()}
        if isinstance(v, list):
            return [fix(x) for x in v]
        return v
    return fix(L)


def build_html(L):
    L = resolve_tokens(L)
    W, Hh = L['size']
    css_fonts = ''.join(f"<link href='https://fonts.googleapis.com/css2?family={f.replace(' ', '+')}:wght@400;700;900&display=swap' rel='stylesheet'>" for f in L.get('fonts', []))
    bg = ''
    if L.get('bg'):
        b64 = base64.b64encode(open(L['bg'], 'rb').read()).decode()
        mime = 'image/png' if L['bg'].lower().endswith('png') else 'image/jpeg'
        bg = f"background-image:url(data:{mime};base64,{b64});background-size:100% 100%;"
    els = []
    over = []
    # v2.1: "images" places files (the logo from the brand kit, a cropped packshot) by percent of the canvas, below the text.
    # v2.2: optional "rotate" (deg), "shadow" (true or a CSS filter), "clip" (CSS clip-path), "over": true (draw above the text), "css" (raw style), "h" (height %)
    for im in L.get('images', []):
        if im.get('html'):   # v2.2: a raw layer (e.g. a soft light pool behind a pack), drawn in order
            (over if im.get('over') else els).append(im['html'])
            continue
        ib64 = base64.b64encode(open(im['src'], 'rb').read()).decode()
        imime = 'image/png' if im['src'].lower().endswith('png') else 'image/jpeg'
        ist = f"position:absolute;left:{im['x']}%;top:{im['y']}%;width:{im['w']}%;"
        if im.get('h') is not None:
            ist += f"height:{im['h']}%;object-fit:cover;"
        if im.get('opacity') is not None:
            ist += f"opacity:{im['opacity']};"
        if im.get('rotate'):
            ist += f"transform:rotate({im['rotate']}deg);transform-origin:{im.get('origin', '50% 50%')};"
        if im.get('shadow'):
            ist += "filter:" + (im['shadow'] if isinstance(im['shadow'], str) else "drop-shadow(0 18px 22px rgba(0,0,0,.35))") + ";"
        if im.get('clip'):
            ist += f"clip-path:{im['clip']};"
        ist += im.get('css', '')
        (over if im.get('over') else els).append(f"<img src='data:{imime};base64,{ib64}' style=\"{ist}\">")
    for e in L.get('elements', []):
        fs = e['size'] * Hh / 100
        style = (f"position:absolute;left:{e['x']}%;top:{e['y']}%;width:{e['w']}%;font-family:'{e.get('font', 'Arial Black')}',Impact,'Arial Black',sans-serif;"
                 f"font-size:{fs}px;color:{e.get('color', '#111')};font-weight:{e.get('weight', 900)};text-align:{e.get('align', 'left')};"
                 f"line-height:{e.get('line', 1.05)};letter-spacing:{e.get('track', 0)}em;")
        if e.get('rotate'):
            style += f"transform:rotate({e['rotate']}deg);"
        style += e.get('css', '')
        if e.get('pill'):
            pv, ph = e.get('pad', [1, 3])
            style += f"background:{e['pill']};padding:{pv * Hh / 100}px {ph * W / 100}px;border-radius:{e.get('radius', 99)}px;box-sizing:border-box;width:{e['w']}%;"
        txt = e['text']
        if e.get('mark_bg'):
            txt = txt.replace('<mark>', f"<span style='background:{e['mark_bg']};padding:0 .12em'>").replace('</mark>', '</span>')
        els.append(f"<div style=\"{style}\">{txt}</div>")
    for st in L.get('stacks', []):
        # flow layout: items stack top to bottom inside one box, so a bigger headline pushes the next line down instead of colliding
        kids = []
        for e in st['items']:
            fs = e['size'] * Hh / 100
            sty = (f"font-family:'{e.get('font', 'Arial Black')}',Impact,'Arial Black',sans-serif;font-size:{fs}px;color:{e.get('color', '#111')};"
                   f"font-weight:{e.get('weight', 900)};text-align:{e.get('align', 'left')};line-height:{e.get('line', 1.05)};letter-spacing:{e.get('track', 0)}em;"
                   f"margin-top:{e.get('gap', 0) * Hh / 100}px;" + e.get('css', ''))
            txt = e['text']
            if e.get('mark_bg'):
                txt = txt.replace('<mark>', f"<span style='background:{e['mark_bg']};padding:0 .12em'>").replace('</mark>', '</span>')
            if e.get('pill'):
                pv, ph = e.get('pad', [1, 3])
                sty += f"display:inline-block;background:{e['pill']};padding:{pv * Hh / 100}px {ph * W / 100}px;border-radius:{e.get('radius', 99)}px;"
            kids.append(f"<div style=\"{sty}\">{txt}</div>")
        sst = f"position:absolute;left:{st['x']}%;top:{st['y']}%;width:{st['w']}%;"
        if st.get('rotate'):
            sst += f"transform:rotate({st['rotate']}deg);"
        els.append(f"<div style=\"{sst}{st.get('css', '')}\">{''.join(kids)}</div>")
    return (f"<!doctype html><html><head><meta charset='utf-8'>{css_fonts}<style>html,body{{margin:0;padding:0}}"
            f".c{{position:relative;width:{W}px;height:{Hh}px;overflow:hidden;background:{L.get('bg_color', '#fff')};{bg}}}</style></head>"
            f"<body><div class='c' style=\"{L.get('canvas_css', '')}\">{''.join(els)}{''.join(over)}</div></body></html>")


def main():
    L = json.load(open(sys.argv[1], encoding='utf-8'))
    out = os.path.abspath(sys.argv[2])
    hp = out + '.html'
    open(hp, 'w', encoding='utf-8').write(build_html(L))
    W, Hh = L['size']
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', f'--window-size={W},{Hh}', '--virtual-time-budget=8000',
                    f'--screenshot={out}', 'file:///' + hp.replace('\\', '/')], check=True, capture_output=True, timeout=120)
    os.remove(hp)
    print('ok', out)


if __name__ == '__main__':
    main()
