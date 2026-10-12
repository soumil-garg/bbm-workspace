"""Round-level visual diversity check (QA check 14): does this round look like one ad repeated, or like different ads?

  python round_diversity.py <round>/out | <For Approval folder> | <images...> [--max-share 0.4]

For every image: background family (from the border pixels: black, dark, white, pale (cream, off-white, pale tints), warm neutral (beige, tan, wood), grey, teal/green, yellow/orange, red/pink,
blue/purple, other), a 16x16 layout thumbnail and a colour signature. Reports:
  - background-family counts: no family may hold more than max-share of the round (default 40%, Meta Andromeda keeps similar ads
    from competing, practitioner guidance is similarity under about 40%)
  - near-duplicate pairs (layout and colour almost identical)
  - person / scene variety is NOT measured here: tag it by eye (studio, lifestyle, native, graphic, people) and keep at least 3 of
    those scene types in a round of 6 or more.
Native and UGC-style ads belong to the diversity budget, not the brand-colour budget.
"""
import sys, os, glob, colorsys, collections
from PIL import Image


def family(rgb):
    # v3 (2026-10-10): light grounds are classed by chroma, not HLS saturation (HLS saturation is huge for cream and off-white, which landed them in "yellow/orange"
    # and made the loved Daigo round 4 set fail at 60%); dark warm rooms are "dark" unless the hue is blue (navy stays blue/purple).
    r, g, b = [v / 255 for v in rgb]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    chroma = max(r, g, b) - min(r, g, b)
    d = h * 360
    if l < 0.12:
        return 'black'
    if l > 0.93 and chroma < 0.1:
        return 'white'
    if l > 0.78 and chroma < 0.3:
        return 'pale'
    if chroma < 0.1:
        return 'grey' if l >= 0.28 else 'dark'
    if l < 0.3 and not (190 <= d < 290):
        return 'dark'
    if 10 <= d < 70 and chroma < 0.4:
        return 'warm neutral'      # beige, tan, wood, warm rooms; only saturated yellow and orange count as yellow/orange
    if d < 15 or d >= 335:
        return 'red/pink'
    if d < 70:
        return 'yellow/orange'
    if d < 170:
        return 'teal/green'
    if d < 290:
        return 'blue/purple'
    return 'red/pink'


def bg_of(im):
    w, h = im.size
    px = []
    for x in range(0, w, max(w // 40, 1)):
        px += [im.getpixel((x, 2)), im.getpixel((x, h - 3))]
    for y in range(0, h, max(h // 40, 1)):
        px += [im.getpixel((2, y)), im.getpixel((w - 3, y))]
    return tuple(sum(c[i] for c in px) // len(px) for i in range(3)), family(tuple(sum(c[i] for c in px) // len(px) for i in range(3)))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    share = 0.4
    if '--max-share' in sys.argv:
        share = float(sys.argv[sys.argv.index('--max-share') + 1])
        args = [a for a in args if a != str(share)]
    files = []
    for a in args:
        files += sorted(glob.glob(os.path.join(a, '*.png')) + glob.glob(os.path.join(a, '*.jpg'))) if os.path.isdir(a) else [a]
    files = [f for f in files if 'sheet' not in os.path.basename(f).lower()]      # contact sheets are not pictures
    if not files:
        sys.exit('ERROR: 0 images found (pass the folder that holds the pictures: <round>/out or the For Approval folder)')
    data = []
    for f in files:
        im = Image.open(f).convert('RGB')
        rgb, fam = bg_of(im)
        data.append((os.path.basename(f), fam, rgb, [tuple(b[i:i + 3]) for b in [im.resize((16, 16)).tobytes()] for i in range(0, len(b), 3)]))
    fams = collections.Counter(d[1] for d in data)
    n = len(data)
    verdict = 'PASS'
    print(f'{n} images')
    for fam, c in fams.most_common():
        flag = ''
        if n >= 4 and c / n > share:
            flag = f'  <- over {int(share * 100)}% of the round'
            verdict = 'FAIL'
        print(f'  background {fam}: {c} ({round(100 * c / n)}%){flag}')
    dup = []
    for i in range(n):
        for j in range(i + 1, n):
            diff = sum(abs(a - b) for p, q in zip(data[i][3], data[j][3]) for a, b in zip(p, q)) / (16 * 16 * 3 * 255)
            if diff < 0.06:
                dup.append((data[i][0], data[j][0], round(diff, 3)))
    for d in dup:
        print('  near-duplicate:', *d)
    if dup and verdict == 'PASS':
        verdict = 'REVIEW'
    print(verdict)


if __name__ == '__main__':
    main()
