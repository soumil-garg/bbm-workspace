"""QA numbers for round 1: product separation (check 12), brand fit (13), round diversity (14)."""
import json, subprocess, os, glob, sys
from PIL import Image
SK = 'C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg/scripts'
ROOT = 'C:/cca/daigo'
IDS = ['T1_A_TrainBerth', 'T1_T_Type', 'T1_U_Berth', 'T2_M_Steps', 'T2_U_Cardboard', 'T3_H_Bag', 'T3_T_Sachets', 'T4_N_Desk', 'T4_U_Cupboard', 'T5_N_Notes', 'T5_U_Notebook',
       'M6_S_Offer', 'M6_P_Price', 'B8_S_Offer', 'B8_M_Count', 'B9_S_Offer', 'B9_M_Count']
NATIVE = {'T1_A_TrainBerth', 'T1_U_Berth', 'T2_U_Cardboard', 'T4_N_Desk', 'T4_U_Cupboard', 'T5_U_Notebook'}
f = lambda v: v / 255 / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
Lum = lambda c: 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])


def mean(im, box):
    W, H = im.size
    b = [int(max(0, min(1, v)) * s) for v, s in zip(box, (W, H, W, H))]
    c = im.crop(b).resize((1, 1)).getpixel((0, 0))
    return c


print('== check 12: product separation (pack body vs the background next to it; need >= 3:1, below 2:1 is a hard fail)')
for i in IDS:
    L = json.load(open(ROOT + '/layouts/%s.json' % i, encoding='utf-8'))
    pk = [m for m in L.get('images', []) if m['src'].endswith('pack_masala_top_cut.png')]
    if not pk:
        continue
    m = pk[0]
    im = Image.open(ROOT + '/img/%s.png' % i).convert('RGB')
    x, y, w = m['x'] / 100, m['y'] / 100, m['w'] / 100
    h = w * 0.858
    body = mean(im, (x + 0.3 * w, y + 0.28 * h, x + 0.7 * w, min(1, y + 0.62 * h)))
    # background: the strip left of the pack, else right; clipped to the canvas
    if x > 0.08:
        bg = mean(im, (x - 0.06, y + 0.1 * h, x - 0.01, min(1, y + 0.5 * h)))
    else:
        bg = mean(im, (x + w + 0.01, y + 0.1 * h, x + w + 0.06, min(1, y + 0.5 * h)))
    l1, l2 = Lum(body), Lum(bg)
    r = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
    print('%-18s body %s bg %s ratio %.1f %s' % (i, body, bg, r, 'PASS' if r >= 3 else ('FAIL (hard)' if r < 2 else 'RISK')))

print('\n== check 13: brand fit (designed ads against the kit; scenes with --native)')
for i in IDS:
    cmd = ['python', SK + '/brand_kit.py', 'check', ROOT + '/kit/brand-kit.json', ROOT + '/img/%s.png' % i] + (['--native'] if i in NATIVE else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    print(i, '|', ' / '.join(l.strip() for l in out[-3:])[:230])
