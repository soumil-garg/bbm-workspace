"""Build a clean reference sheet: product packshots on white in a grid. No captions, no props.
Usage: python build_reference.py <out.jpg> <img1> <img2> ... [--cols 4] [--cell 520]
Pass packshot-only images (product on plain background). If a packshot has props (fruit, leaves, badges,
'as seen on' stickers), crop them out first: props in the reference leak into generated ads.
Transparent PNGs are flattened onto white.
"""
import argparse
from PIL import Image

ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('imgs', nargs='+')
ap.add_argument('--cols', type=int, default=4); ap.add_argument('--cell', type=int, default=520)
a = ap.parse_args()
W = a.cell
rows = (len(a.imgs) + a.cols - 1) // a.cols
s = Image.new('RGB', (W * min(a.cols, len(a.imgs)), W * rows), 'white')
for i, f in enumerate(a.imgs):
    im = Image.open(f).convert('RGBA')
    bg = Image.new('RGBA', im.size, 'white'); bg.alpha_composite(im); im = bg.convert('RGB')
    im.thumbnail((W - 20, W - 20))
    s.paste(im, ((i % a.cols) * W + (W - im.width) // 2, (i // a.cols) * W + (W - im.height) // 2))
s.save(a.out, quality=90)
print('saved', a.out, s.size)
