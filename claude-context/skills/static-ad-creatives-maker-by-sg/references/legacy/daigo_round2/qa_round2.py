"""QA numbers for round 2: product separation (check 12), brand fit (13), round diversity (14).
  python qa_round2.py"""
import json, subprocess, os, glob, sys
import numpy as np
from PIL import Image
SK = 'C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg/scripts'
R2 = 'C:/cca/daigo/round2'
IDS = sorted(os.path.basename(f)[:-5] for f in glob.glob(R2 + '/layouts/R2_*.json'))
NATIVE = set(a for a in IDS if '_L_' in a or any(k in a for k in ('Chat', 'Hostel', 'Train', 'PG', 'Steps', 'Roof', 'Roommates')))   # real-scene photos with a designed band: exempt from the colour check, product and logo rules still apply
f = lambda v: v / 255 / 12.92 if v / 255 <= 0.03928 else ((v / 255 + 0.055) / 1.055) ** 2.4
Lum = lambda c: 0.2126 * f(c[0]) + 0.7152 * f(c[1]) + 0.0722 * f(c[2])

# the PLAIN blue band of the real pack crop (QA gate 12: a region with lettering reads too light)
_a = np.array(Image.open('C:/cca/daigo/assets/pack_masala_top_cut_clean.png').convert('RGBA')).astype(float)
_m = (_a[..., 3] > 240) & (_a[..., 2] > _a[..., 0] + 60) & (_a[..., 2] > _a[..., 1] + 40)
BLUE = tuple(int(v) for v in _a[_m][:, :3].mean(axis=0))


def mean(im, box):
    W, H = im.size
    b = [int(max(0, min(1, v)) * s) for v, s in zip(box, (W, H, W, H))]
    return im.crop(b).resize((1, 1)).getpixel((0, 0))


print("== check 12: product separation. The pack's plain blue band", BLUE, 'against the strips left, right and above the pack; worst of them (need >= 3:1, below 2:1 is a hard fail)')
for i in IDS:
    L = json.load(open(R2 + '/layouts/%s.json' % i, encoding='utf-8'))
    pk = [m for m in L.get('images', []) if 'pack_masala_top_cut' in str(m.get('src', ''))]
    if not pk:
        continue
    m = pk[0]
    im = Image.open(R2 + '/img/%s.png' % i).convert('RGB')
    x, y, w = m['x'] / 100, m['y'] / 100, m['w'] / 100
    h = w * 0.858
    left = (x - 0.05, y + 0.1 * h, x - 0.005, min(1, y + 0.5 * h))
    right = (x + w + 0.005, y + 0.1 * h, x + w + 0.05, min(1, y + 0.5 * h))
    above = (x + 0.2 * w, y - 0.05, x + 0.8 * w, y - 0.005)
    out = []
    for name, box in (('left', left), ('right', right), ('above', above)):
        if box[0] < 0 or box[2] > 1 or box[1] < 0:
            continue
        bg = mean(im, box)
        l1, l2 = Lum(BLUE), Lum(bg)
        out.append((name, (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)))
    g = min(r for n, r in out) if out else 0
    print('%-16s %s | worst %.1f %s' % (i, ', '.join('%s %.1f' % t for t in out), g, 'PASS' if g >= 3 else ('FAIL (hard)' if g < 2 else 'RISK')))

print()
print('== check 13: brand fit (designed ads against the kit; photo posters and chat with --native)')
for i in IDS:
    cmd = ['python', SK + '/brand_kit.py', 'check', 'C:/cca/daigo/kit/brand-kit.json', R2 + '/img/%s.png' % i] + (['--native'] if i in NATIVE else [])
    r = subprocess.run(cmd, capture_output=True, text=True)
    out = (r.stdout + r.stderr).strip().splitlines()
    print('%-16s %s' % (i, out[0] if out else '?'))

print()
print('== check 14: round diversity')
r = subprocess.run(['python', SK + '/round_diversity.py'] + [R2 + '/img/%s.png' % i for i in IDS], capture_output=True, text=True)
print((r.stdout + r.stderr).strip()[-1800:])
