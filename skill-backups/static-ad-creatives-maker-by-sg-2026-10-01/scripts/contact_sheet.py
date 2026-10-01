"""Contact sheet of all PNG/JPG in a folder, with filenames as labels.
Usage: python contact_sheet.py <folder> <out.jpg> [--cols 4] [--width 420] [--prefix Habbits_]
"""
import argparse, glob, os
from PIL import Image, ImageDraw, ImageFont

ap = argparse.ArgumentParser()
ap.add_argument('folder'); ap.add_argument('out')
ap.add_argument('--cols', type=int, default=4); ap.add_argument('--width', type=int, default=420)
ap.add_argument('--prefix', default='')
a = ap.parse_args()
fs = sorted(f for f in glob.glob(os.path.join(a.folder, '*.png')) + glob.glob(os.path.join(a.folder, '*.jpg'))
            if 'contact_sheet' not in os.path.basename(f))
if not fs:
    raise SystemExit('no images')
try:
    F = ImageFont.truetype('arial.ttf', 16)
except Exception:
    F = None
W, LH = a.width, 26
rows = (len(fs) + a.cols - 1) // a.cols
s = Image.new('RGB', (W * a.cols, (W + LH) * rows), 'white')
d = ImageDraw.Draw(s)
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB'); im.thumbnail((W, W))
    x, y = (i % a.cols) * W, (i // a.cols) * (W + LH)
    s.paste(im, (x, y + LH))
    name = os.path.splitext(os.path.basename(f))[0].replace(a.prefix, '')
    d.text((x + 6, y + 5), name, fill='black', font=F)
s.save(a.out, quality=90)
print(len(fs), 'images ->', a.out)
