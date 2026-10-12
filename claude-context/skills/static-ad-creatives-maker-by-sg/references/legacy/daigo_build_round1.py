"""Daigo round 1 build (2026-10-09). The model draws SCENES only (no pack, no text). Code places the REAL pack crop, the logo files and every approved word.
  python build_round1.py prompts            -> p\\<ID>.txt for every scene
  python build_round1.py gen [ID ...]       -> calls gen_image.py for the scenes (parallel)
  python build_round1.py render [ID ...]    -> writes layouts\\<ID>.json and renders img\\<ID>.png with render_ad.py
Copy comes from copy\\copy_v2.json (never retyped). Colours only from kit\\brand-kit.json tokens (raw HTML uses tok(), which errors on an unknown colour)."""
import json, os, re, sys, subprocess, random
from concurrent.futures import ThreadPoolExecutor

ROOT = 'C:/cca/daigo'
SK = 'C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg/scripts'
KITP = ROOT + '/kit/brand-kit.json'
KIT = json.load(open(KITP, encoding='utf-8'))
PAL = {**KIT['colors'], **KIT['flex']}
COPY = json.load(open(ROOT + '/copy/copy_v2.json', encoding='utf-8'))
C = {c['id']: c for c in COPY['concepts']}
PACK = ROOT + '/assets/pack_masala_top_cut.png'
LB = ROOT + '/ref/logo_new_01.png'   # transparent wordmark, light backgrounds
LW = ROOT + '/ref/logo_new_02.png'   # white wordmark on its own blue block
FONTS = ['Baloo 2', 'Poppins', 'Caveat']
SIZE = [1080, 1080]
for d in ('p', 'img', 'layouts'):
    os.makedirs(ROOT + '/' + d, exist_ok=True)


def tok(n):
    if n not in PAL:
        raise SystemExit('colour not in the brand kit: ' + n)
    return PAL[n]


def H(cid):
    return C[cid]['headline']


def S(cid):
    return C[cid]['sub']


def sentences(h):
    return [s.strip() for s in re.split(r'(?<=[.!?])\s+', h) if s.strip()]


def scene(i):
    return ROOT + '/img/scene_%s.png' % i


def pack(x, y, w, rot=0, over=False):
    return {'src': PACK, 'x': x, 'y': y, 'w': w, 'rotate': rot, 'shadow': True, 'over': over}


def glow(cx, cy, size, a=0.45):
    # a soft light pool behind a pack so the blue body separates from the background (QA check 12); cx, cy, size in percent of the canvas
    px = size * 10.8
    return {'html': "<div style=\"position:absolute;left:%s%%;top:%s%%;width:%dpx;height:%dpx;margin:-%dpx 0 0 -%dpx;background:radial-gradient(closest-side, rgba(255,255,255,%s), rgba(255,255,255,0));\"></div>" % (cx, cy, px, px, px / 2, px / 2, a)}


def logo(x, y, w, kind='blue'):
    return {'src': LB if kind == 'blue' else LW, 'x': x, 'y': y, 'w': w}


def scrim(h_pct, top=True, a=0.7):
    d = 'to bottom' if top else 'to top'
    y = 0 if top else 100 - h_pct
    return {'text': '', 'x': 0, 'y': y, 'w': 100, 'size': 1,
            'css': 'height:%s%%;background:linear-gradient(%s, rgba(12,20,46,%s), rgba(12,20,46,0));' % (h_pct, d, a)}


def base(**kw):
    L = {'kit': KITP, 'size': SIZE, 'fonts': FONTS, 'images': [], 'elements': [], 'stacks': []}
    L.update(kw)
    return L


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
    return {'text': "<div style='display:grid;grid-template-columns:repeat(%d,1fr);gap:%s%% %s%%'>%s</div>" % (cols, gap_pct, gap_pct * 0.9, cells),
            'x': x, 'y': y, 'w': w, 'size': 1}


def badge(n, x, y, size_pct, bgc='navy', fg='white'):
    px = size_pct * 10.8
    return {'text': "<div style=\"width:%dpx;height:%dpx;border-radius:50%%;background:%s;color:%s;font:800 %dpx 'Baloo 2';display:flex;align-items:center;justify-content:center;box-shadow:0 4px 10px rgba(0,0,0,.25)\">%s</div>" % (
        px, px, tok(bgc), tok(fg), px * 0.62, n), 'x': x, 'y': y, 'w': size_pct, 'size': 1}


def sticker(count, x, y, size_pct, rot=-8):
    px = size_pct * 10.8
    return {'text': "<div style=\"width:%dpx;height:%dpx;border-radius:50%%;background:%s;display:flex;flex-direction:column;align-items:center;justify-content:center;box-shadow:0 8px 16px rgba(0,0,0,.28);transform:rotate(%sdeg)\">"
                    "<div style=\"font:800 %dpx 'Baloo 2';color:%s;line-height:.85\">%s</div><div style=\"font:800 %dpx 'Baloo 2';color:%s;letter-spacing:.04em\">SACHETS</div></div>" % (
                        px, px, tok('jaljira_yellow'), rot, px * 0.42, tok('navy'), count, px * 0.17, tok('navy')), 'x': x, 'y': y, 'w': size_pct, 'size': 1}


def tick(px, col):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40' width='%d' height='%d'><circle cx='20' cy='20' r='19' fill='%s'/>"
            "<path d='M11 21 L18 28 L30 13' fill='none' stroke='#FFFFFF' stroke-width='4.5' stroke-linecap='round' stroke-linejoin='round'/></svg>") % (px, px, col)


def hand_tick(px, col):
    return ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 40 40' width='%d' height='%d'><path d='M5 22 L15 33 L36 7' fill='none' stroke='%s' stroke-width='4.2' stroke-linecap='round' stroke-linejoin='round'/></svg>") % (px, px, col)


# ------------------------------------------------------------------ scene prompts (the model draws scenes only)
SUF = (" [NO TEXT] Absolutely no text, letters, numbers, logos, brand names, labels or watermarks anywhere in the image; every foil sachet, bottle and box is completely plain."
       " [NO PLATFORM CHROME] A standalone photograph only: no phone frame, no status bar, no captions."
       " [EDGE-SAFE] Keep every important object inside the central 84% of the frame.")
SCENES = {
    'T1_A_TrainBerth': ('1024x1024',
        "A real photograph, square. Inside an Indian train compartment at golden hour: a close view of a fold-down tray table beside a window. On the tray stand one tall steel tumbler of pale creamy chaas (buttermilk) "
        "with a sprig of mint and light condensation, and one torn-open plain silver foil sachet lying next to it. Through the window a blurred warm countryside and a few blurred station lights. "
        "Natural warm light, shallow depth of field, slight grain, phone-camera realism, Indian train interior details (blue-grey seat vinyl, dark window frame). No people. "
        "Keep the top 40% of the frame calm (soft window glow and dark window frame) and leave the bottom-left corner of the tray empty."),
    'T1_U_Berth': ('1024x1024',
        "A casual, slightly crooked smartphone photo taken with the on-camera flash, looking down at a thin folding tray on a train upper berth: a steel glass of pale chaas, a torn plain silver foil sachet, "
        "a crumpled tissue and a phone charger cable. Harsh flash glare, grainy, slightly overexposed, amateur composition. No people. Keep the top 38% of the frame as a plain blurred train wall."),
    'T2_M_Steps': ('1536x1024',
        "A clean horizontal photo triptych made of exactly three equal panels side by side, separated by thin warm-white gaps. The same soft warm kitchen daylight and the same Indian hands (medium skin tone) in all three panels. "
        "Left panel: two hands tearing open the notch of a plain silver foil sachet held above the mouth of a clear plastic shaker bottle. Middle panel: white powder with tiny green flecks and a stream of clear water falling into the clear shaker bottle. "
        "Right panel: one hand shaking the closed clear shaker bottle with slight motion blur, a steel glass of pale chaas standing beside it. Plain light neutral backgrounds. Correct anatomy: five fingers on each hand."),
    'T2_U_Cardboard': ('1024x1024',
        "A top-down phone photo of a rough brown cardboard sheet torn from a box, lying on a grey hostel-room floor tile. A few simple marker doodles in black and blue ink only along the edges: a long curling arrow, "
        "the outline of a silver sachet, the outline of a water bottle, the outline of a glass with a squiggle on top. The centre 60% of the cardboard is left empty. Slight flash glare, crooked framing. No letters, no words, no numbers."),
    'T3_H_Bag': ('1024x1024',
        "A real studio-style photograph, square. A single olive-green canvas backpack standing upright against a seamless pale blue-grey background (colour #DCE4F4), photographed straight on at eye level; its large front zip pocket is open at the top "
        "with a few plain silver foil sachets sticking out. Soft even studio light with a gentle floor shadow. The backpack is fairly small in the frame: it stands at the bottom centre with its top handle at about 58% down from the top edge of the frame, with wide margins left and right. The top 55% of the frame is completely empty, plain pale backdrop with nothing in it."),
    'T4_N_Desk': ('1024x1024',
        "A real phone photograph of a study desk in an Indian college hostel room, seen straight on at desk height: a plain light-grey painted wall, a steel water bottle, a steel tumbler, a clear plastic shaker bottle, "
        "a small stack of plain-covered notebooks, an unplugged desk lamp, a torn plain silver foil sachet on the desk. Soft daylight from the left, tidy but lived-in, no people, nothing on the wall. The camera is placed so that the plain wall fills the top 62% of the frame and is completely empty; the desk surface runs along the bottom 28% of the frame with all objects small and low (nothing taller than 14% of the frame height, no lamp raised above the desk top)."),
    'T4_U_Cupboard': ('1024x1024',
        "A phone-flash photo of the closed door of a cheap painted steel hostel cupboard (pale green-grey metal door with scuffs and a rusty lock plate), slightly crooked, harsh flash glare, grainy. "
        "Nothing is stuck on the door and nothing is written on it. The centre 70% of the door is clear and plain."),
    'T5_U_Notebook': ('1024x1024',
        "A phone-camera photo from above: a ruled school notebook lying open on a hostel bed beside a half-packed duffel bag, with a phone charger cable and a toothbrush at the edge of the frame. "
        "The notebook page is completely blank, ruled lines only, a pen lies across the bottom of the page. Natural window light, casual, slightly crooked. The left page of the notebook fills the centre of the frame."),
    'M6_S_Offer': ('1024x1024',
        "A real studio photograph, square, on a seamless flat green paper backdrop (colour #84B355) with a matching green surface. A tall steel tumbler of pale creamy chaas with a mint sprig and light condensation stands at the lower left, "
        "soft even light, a gentle shadow. The top 45% and the right 45% of the frame are empty backdrop."),
    'B8_S_Offer': ('1024x1024',
        "A real studio photograph, square, on a seamless flat warm sand paper backdrop (colour #D8CBA9) with a matching sand surface. A clear tall glass of pale creamy chaas with a mint sprig and light condensation stands at the lower right, "
        "soft even light, a gentle shadow. The top 45% and the left 40% of the frame are empty backdrop."),
    'B9_S_Offer': ('1024x1024',
        "A real studio photograph, square, on a seamless flat pale blue-grey paper backdrop (colour #DCE4F4) with a matching surface. A steel tumbler and next to it a clear glass, both with pale creamy chaas, a mint sprig on the table, "
        "stand at the lower centre-left, soft even light, gentle shadows. The top 45% and the right 40% of the frame are empty backdrop."),
}


def write_prompts():
    for i, (size, body) in SCENES.items():
        open(ROOT + '/p/%s.txt' % i, 'w', encoding='utf-8').write(body + SUF)
    print(len(SCENES), 'scene prompts written')


def gen(ids):
    ids = ids or list(SCENES)

    def one(i):
        size = SCENES[i][0]
        out = scene(i)
        cmd = ['python', SK + '/gen_image.py', '--prompt-file', ROOT + '/p/%s.txt' % i, '--out', out, '--size', size, '--tag', 'daigo_r1_' + i, '--model', 'gpt-image-2.5-sunburst']
        r = subprocess.run(cmd, capture_output=True, text=True)
        return i, (r.stdout + r.stderr).strip()[-200:]
    with ThreadPoolExecutor(6) as ex:
        for i, msg in ex.map(one, ids):
            print(i, '->', msg)


# ------------------------------------------------------------------ layouts (code places the real pack, the logo and all approved words)
def L_T1_A():
    return base(bg=scene('T1_A_TrainBerth'), images=[glow(30, 91, 60, 0.7), pack(18, 80, 24, -3), logo(71, 86, 22, 'white')], elements=[scrim(52, True, 0.72)],
                stacks=[{'x': 8, 'y': 7, 'w': 84, 'items': [
                    {'text': H('N1'), 'size': 8.8, 'font': 'Baloo 2', 'weight': 800, 'color': '$white', 'line': 1.0, 'css': 'text-shadow:0 2px 14px rgba(0,0,0,.45);'},
                    {'text': S('N1'), 'size': 3.3, 'font': 'Poppins', 'weight': 500, 'color': '$white', 'gap': 2.4, 'css': 'text-shadow:0 1px 8px rgba(0,0,0,.55);'}]}])


def L_T1_T():
    h = H('N1')
    assert h == 'For when you miss ghar ki chaas'
    lines = "For when<br>you miss<br><span style='color:$magenta'>ghar ki<br>chaas</span>"
    return base(bg_color='$cream', images=[pack(57, 71, 37, 4), logo(8, 84, 24, 'blue')],
                stacks=[{'x': 8, 'y': 8, 'w': 84, 'items': [
                    {'text': lines, 'size': 13.2, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 0.98},
                    {'text': S('N1'), 'size': 3.4, 'font': 'Poppins', 'weight': 500, 'color': '$ink', 'gap': 2.6}]}])


def L_T1_U():
    return base(bg=scene('T1_U_Berth'), images=[logo(75, 87, 19, 'white')],
                stacks=[{'x': 6, 'y': 6, 'w': 88, 'rotate': -3, 'items': [
                    {'text': H('N1'), 'size': 12.4, 'font': 'Caveat', 'weight': 700, 'color': '$white', 'line': 0.95,
                     'css': 'text-shadow:-3px -3px 0 #000,3px -3px 0 #000,-3px 3px 0 #000,3px 3px 0 #000,0 6px 14px rgba(0,0,0,.5);'}]}],
                elements=[{'text': S('N1'), 'x': 7, 'y': 81, 'w': 62, 'size': 3.1, 'font': 'Poppins', 'weight': 600, 'color': '$ink', 'pill': '$white', 'pad': [1.2, 2.6], 'radius': 18,
                           'rotate': 1.5, 'line': 1.2}])


def L_T2_M():
    ims = [{'src': scene('T2_M_Steps'), 'x': 14, 'y': 35, 'w': 72}, logo(75, 86.5, 18, 'blue')]
    els = [badge(str(k + 1), 14 + k * 24 + 1.0, 36.2, 4.8) for k in range(3)]
    return base(bg_color='$cream', images=ims, elements=els + [
        {'text': S('N2'), 'x': 8, 'y': 87.5, 'w': 60, 'size': 3.6, 'font': 'Poppins', 'weight': 500, 'color': '$ink'}],
        stacks=[{'x': 8, 'y': 5, 'w': 84, 'items': [{'text': 'Tear. Pour.<br>Shake.', 'size': 12.4, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'align': 'center', 'line': 1.0}]}])


def L_T2_U():
    return base(bg=scene('T2_U_Cardboard'), images=[logo(75, 87, 18, 'white')],
                stacks=[{'x': 7, 'y': 25, 'w': 86, 'rotate': -4, 'items': [
                    {'text': 'Tear. Pour.<br>Shake.', 'size': 15, 'font': 'Caveat', 'weight': 700, 'color': '#1A1A1A', 'align': 'center', 'line': 0.95}]},
                    {'x': 15, 'y': 62, 'w': 58, 'rotate': 2, 'items': [
                    {'text': S('N2'), 'size': 5.6, 'font': 'Caveat', 'weight': 700, 'color': '#16337A', 'align': 'center', 'line': 1.0}]}])


def L_T3_H():
    return base(bg_color='$blue_light', images=[{'src': scene('T3_H_Bag'), 'x': 0, 'y': 4, 'w': 100, 'css': 'mask-image:linear-gradient(to bottom, transparent 0, #000 9%, #000 100%);-webkit-mask-image:linear-gradient(to bottom, transparent 0, #000 9%, #000 100%);'}, glow(81, 90, 40, 0.5), pack(70, 78, 22, 3), logo(8, 85, 22, 'blue')],
                stacks=[{'x': 5, 'y': 5, 'w': 90, 'items': [
                    {'text': '10 sachets.<br>10 glasses of chaas.', 'size': 7.9, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'align': 'center', 'line': 1.0},
                    {'text': S('N3'), 'size': 3.4, 'font': 'Poppins', 'weight': 500, 'color': '$ink', 'align': 'center', 'gap': 2.0}]}])


def L_T3_T():
    return base(bg_color='$green_light', images=[logo(70, 85, 22, 'blue')],
                elements=[sachet_grid(10, 5, 8, 50, 62, 3.4)],
                stacks=[{'x': 8, 'y': 8, 'w': 84, 'items': [
                    {'text': '10 sachets.<br>10 glasses<br>of chaas.', 'size': 11.0, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 1.0},
                    {'text': S('N3'), 'size': 3.6, 'font': 'Poppins', 'weight': 500, 'color': '$ink', 'gap': 2.6}]}])


def L_T4_N():
    return base(bg=scene('T4_N_Desk'), images=[logo(75, 87, 19, 'white')],
                stacks=[{'x': 8, 'y': 5, 'w': 84, 'items': [
                    {'text': '<br>'.join(sentences(H('N4'))), 'size': 7.6, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 1.0},
                    {'text': S('N4'), 'size': 3.2, 'font': 'Poppins', 'weight': 500, 'color': '$ink', 'gap': 1.8, 'css': 'max-width:76%;'}]}])


def note(text, x, y, w, rot, px_size):
    return {'text': "<div style=\"width:100%%;aspect-ratio:3/2;background:#F6E36A;box-shadow:0 10px 18px rgba(0,0,0,.35);display:flex;align-items:center;justify-content:center;text-align:center;padding:0 6%%;"
                    "font:700 %dpx Caveat;color:#2A2A2A;line-height:1;transform:rotate(%sdeg)\">%s</div>" % (px_size * 10.8, rot, text), 'x': x, 'y': y, 'w': w, 'size': 1}


def L_T4_U():
    s = sentences(H('N4'))
    return base(bg=scene('T4_U_Cupboard'), images=[logo(77, 89.5, 17, 'white')],
                elements=[note(s[0], 11, 9, 40, -3, 6.2), note(s[1], 30, 32, 40, 2.2, 6.2), note(s[2], 13, 55, 40, -1.6, 6.8),
                          {'text': "<div style=\"width:100%%;background:#FFFFFF;box-shadow:0 8px 14px rgba(0,0,0,.3);padding:5%% 6%%;font:700 %dpx Caveat;color:#16337A;line-height:1.05;transform:rotate(2deg)\">%s</div>" % (3.8 * 10.8, S('N4')),
                           'x': 33, 'y': 76, 'w': 38, 'size': 1}])


def L_T5_N():
    t, rest = H('N5').split(': ', 1)
    items = [x.strip().capitalize() for x in rest.split(',')]
    rows = ''.join("<div style=\"display:flex;align-items:center;gap:3.2%%;margin-bottom:5.2%%\"><div style='flex:none'>%s</div><div style=\"font:%s %dpx Poppins;color:%s\">%s</div></div>" % (
        tick(64, tok('chaas_green')), '600' if k == 2 else '500', 5.6 * 10.8, tok('ink'), it) for k, it in enumerate(items))
    return base(bg_color='$paper', canvas_css='background-image:repeating-linear-gradient(to bottom, transparent 0, transparent 69px, rgba(32,72,152,.10) 69px, rgba(32,72,152,.10) 70px);',
                images=[pack(52, 70, 40, 3), logo(8, 86, 22, 'blue')],
                elements=[{'text': "<div style=\"font:600 %dpx Poppins;color:%s;border-bottom:3px solid %s;padding-bottom:2%%\">%s</div>" % (8.4 * 10.8, tok('ink'), tok('ink'), t), 'x': 8, 'y': 9, 'w': 60, 'size': 1},
                          {'text': rows, 'x': 8, 'y': 27, 'w': 70, 'size': 1},
                          {'text': S('N5'), 'x': 8, 'y': 69, 'w': 40, 'size': 3.4, 'font': 'Poppins', 'weight': 500, 'color': '$ink'}])


def L_T5_U():
    t, rest = H('N5').split(': ', 1)
    items = [x.strip() for x in rest.split(',')]
    blue = '#1D3FA3'
    rows = ''.join("<div style=\"display:flex;align-items:center;gap:3%%;margin-bottom:1.2%%\"><div style='flex:none'>%s</div><div style=\"font:700 %dpx Caveat;color:%s\">%s</div></div>" % (
        hand_tick(46, blue), 7.0 * 10.8, blue, it) for it in items)
    return base(bg=scene('T5_U_Notebook'), images=[glow(79, 90, 46, 0.55), pack(64, 72, 30, 4), logo(8, 88, 18, 'white')],
                elements=[{'text': "<div style=\"transform:rotate(-2deg)\"><div style=\"font:700 %dpx Caveat;color:%s;border-bottom:4px solid %s;display:inline-block;margin-bottom:2%%\">%s</div>%s</div>" % (
                    8.4 * 10.8, blue, blue, t, rows), 'x': 22, 'y': 38, 'w': 44, 'size': 1},
                    {'text': "<div style=\"transform:rotate(-1deg);font:700 %dpx Caveat;color:%s\">%s</div>" % (4.4 * 10.8, blue, S('N5')), 'x': 57, 'y': 52, 'w': 34, 'size': 1}])


def L_M6_S():
    return base(bg=scene('M6_S_Offer'), images=[glow(72, 90, 78, 0.72), pack(50, 66, 44, 5), logo(73, 5, 21, 'blue')], elements=[sticker('10', 74, 47, 18, -8)],
                stacks=[{'x': 8, 'y': 8, 'w': 60, 'items': [
                    {'text': H('N6'), 'size': 9.0, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 1.0},
                    {'text': S('N6'), 'size': 4.0, 'font': 'Poppins', 'weight': 600, 'color': '$navy', 'gap': 2.4}]}])


def L_M6_P():
    sub = S('N6').replace('Rs 279', "<span style='color:$magenta'>Rs 279</span>")
    return base(bg_color='$paper', images=[pack(53, 67, 41, 3), logo(8, 85, 24, 'blue')],
                stacks=[{'x': 8, 'y': 9, 'w': 84, 'items': [
                    {'text': 'Rs 28', 'size': 30, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 0.9},
                    {'text': 'a glass on the 10-pack', 'size': 7.2, 'font': 'Baloo 2', 'weight': 700, 'color': '$navy', 'gap': 0.5},
                    {'text': sub, 'size': 4.4, 'font': 'Poppins', 'weight': 600, 'color': '$ink', 'gap': 4.5}]}])


def L_B8_S():
    return base(bg=scene('B8_S_Offer'), images=[glow(22, 92, 56, 0.5), pack(3, 67, 38, -4), logo(73, 5, 21, 'blue')], elements=[sticker('20', 31, 57, 17, 8),
                {'text': S('N8'), 'x': 8, 'y': 43.5, 'w': 56, 'size': 3.0, 'font': 'Poppins', 'weight': 600, 'color': '$cream', 'pill': '$navy', 'pad': [1.2, 2.8], 'radius': 40, 'line': 1.2}],
                stacks=[{'x': 8, 'y': 8, 'w': 60, 'items': [{'text': '<br>'.join(sentences(H('N8'))), 'size': 10.6, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 1.0}]}])


def L_B8_M():
    return base(bg_color='$blue_light', images=[logo(70, 86, 22, 'blue')], elements=[sachet_grid(20, 10, 8, 43, 84, 3.0, seed=5),
                {'text': S('N8'), 'x': 8, 'y': 76, 'w': 74, 'size': 3.0, 'font': 'Poppins', 'weight': 600, 'color': '$cream', 'pill': '$navy', 'pad': [1.3, 3.0], 'radius': 40, 'line': 1.2}],
                stacks=[{'x': 8, 'y': 8, 'w': 84, 'items': [{'text': '20 sachets.<br>20 glasses.<br>Rs 529.', 'size': 10.2, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 1.0}]}])


def L_B9_S():
    return base(bg=scene('B9_S_Offer'), images=[glow(76, 92, 56, 0.5), pack(56, 66, 40, 5), logo(73, 5, 21, 'blue')], elements=[sticker('30', 76, 45, 17, -8)],
                stacks=[{'x': 8, 'y': 8, 'w': 62, 'items': [
                    {'text': '<br>'.join(sentences(H('N9'))), 'size': 10.2, 'font': 'Baloo 2', 'weight': 800, 'color': '$navy', 'line': 1.0},
                    {'text': S('N9'), 'size': 4.2, 'font': 'Poppins', 'weight': 600, 'color': '$navy', 'gap': 2.4}]}])


def L_B9_M():
    # flipped layout (grid on top, headline below) on navy, so it does not read as a twin of the 10-sachet type ad
    return base(bg_color='$navy', images=[logo(74, 86, 19, 'white')], elements=[sachet_grid(30, 10, 8, 8, 84, 3.0, seed=9)],
                stacks=[{'x': 8, 'y': 50, 'w': 84, 'items': [
                    {'text': '30 sachets.<br>30 glasses.<br>Rs 749.', 'size': 9.6, 'font': 'Baloo 2', 'weight': 800, 'color': '$white', 'line': 1.0},
                    {'text': S('N9'), 'size': 4.2, 'font': 'Poppins', 'weight': 600, 'color': '$cream', 'gap': 2.4}]}])


LAYOUTS = {
    'T1_A_TrainBerth': L_T1_A, 'T1_T_Type': L_T1_T, 'T1_U_Berth': L_T1_U,
    'T2_M_Steps': L_T2_M, 'T2_U_Cardboard': L_T2_U,
    'T3_H_Bag': L_T3_H, 'T3_T_Sachets': L_T3_T,
    'T4_N_Desk': L_T4_N, 'T4_U_Cupboard': L_T4_U,
    'T5_N_Notes': L_T5_N, 'T5_U_Notebook': L_T5_U,
    'M6_S_Offer': L_M6_S, 'M6_P_Price': L_M6_P,
    'B8_S_Offer': L_B8_S, 'B8_M_Count': L_B8_M,
    'B9_S_Offer': L_B9_S, 'B9_M_Count': L_B9_M,
}


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
        lp = ROOT + '/layouts/%s.json' % i
        json.dump(L, open(lp, 'w', encoding='utf-8'), indent=1)
        r = subprocess.run(['python', SK + '/render_ad.py', lp, ROOT + '/img/%s.png' % i], capture_output=True, text=True)
        print(i, (r.stdout + r.stderr).strip()[-160:])


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    ids = sys.argv[2:]
    {'prompts': lambda: write_prompts(), 'gen': lambda: gen(ids), 'render': lambda: render(ids)}[cmd]()
