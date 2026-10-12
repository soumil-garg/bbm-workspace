"""Cut the real masala pouch top crop out of its white background (RGBA PNG), so code can place the REAL pack in any scene."""
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

def cut(src, dst, thr=247):
    im = Image.open(src).convert('RGB')
    a = np.array(im)
    bg = (a.min(axis=2) >= thr)
    h, w = bg.shape
    seen = np.zeros_like(bg, dtype=bool)
    from collections import deque
    dq = deque()
    for x in range(w):
        for y in (0, h - 1):
            if bg[y, x] and not seen[y, x]:
                seen[y, x] = True; dq.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if bg[y, x] and not seen[y, x]:
                seen[y, x] = True; dq.append((y, x))
    while dq:
        y, x = dq.popleft()
        for ny, nx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
            if 0 <= ny < h and 0 <= nx < w and bg[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True; dq.append((ny, nx))
    m = np.where(seen, 128, 0)
    alpha = np.where(m == 128, 0, 255).astype('uint8')
    al = Image.fromarray(alpha).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    out = im.convert('RGBA')
    out.putalpha(al)
    bbox = al.point(lambda v: 255 if v > 8 else 0).getbbox()
    out = out.crop(bbox)
    out.save(dst)
    print(dst, out.size)

cut('C:/cca/daigo/ref/pack_masala_top.jpg', 'C:/cca/daigo/assets/pack_masala_top_cut.png')
cut('C:/cca/daigo/ref/pack_jaljira_top.jpg', 'C:/cca/daigo/assets/pack_jaljira_top_cut.png')
# preview on navy
for n in ('pack_masala_top_cut',):
    p = Image.open('C:/cca/daigo/assets/%s.png' % n)
    bgc = Image.new('RGBA', (p.width + 80, p.height + 80), (28, 47, 107, 255))
    bgc.alpha_composite(p, (40, 40))
    bgc.convert('RGB').save('C:/cca/daigo/assets/_preview_%s.jpg' % n, quality=92)
