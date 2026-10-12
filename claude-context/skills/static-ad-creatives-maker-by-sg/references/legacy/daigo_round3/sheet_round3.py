"""Numbered contact sheets for Gate 3: a big red number badge in the header strip above every image (never on top of the picture), plus the id and a short label.
  python sheet_round2.py out.jpg W cols  NUMBER:ID:label  NUMBER:ID:label ...      (images from round2\\img\\<ID>.png)"""
import sys
from PIL import Image, ImageDraw, ImageFont

out, W, cols = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
items = [a.split(':', 2) for a in sys.argv[4:]]
HDR = 46
rows = (len(items) + cols - 1) // cols
sheet = Image.new('RGB', (cols * W, rows * (W + HDR)), 'white')
d = ImageDraw.Draw(sheet)
fb = ImageFont.truetype('arialbd.ttf', 26)
fs = ImageFont.truetype('arial.ttf', 17)
for k, (num, i, label) in enumerate(items):
    im = Image.open('C:/cca/daigo/round3/out/%s.png' % i).convert('RGB')
    im.thumbnail((W - 6, W - 6))
    x, y = (k % cols) * W, (k // cols) * (W + HDR)
    d.ellipse((x + 6, y + 4, x + 6 + 38, y + 4 + 38), fill=(200, 25, 35))
    tw = d.textlength(num, font=fb)
    d.text((x + 6 + (38 - tw) / 2, y + 7), num, fill='white', font=fb)
    d.text((x + 52, y + 5), i, fill='black', font=fs)
    d.text((x + 52, y + 24), label, fill=(90, 90, 90), font=fs)
    sheet.paste(im, (x + 3, y + HDR))
sheet.save(out, quality=90)
print(out, sheet.size)
