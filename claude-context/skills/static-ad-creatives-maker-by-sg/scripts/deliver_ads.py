"""deliver_ads.py: package a round the same way every time (v3, 2026-10-10, as delivered for Daigo round 4).
  python <skill>/scripts/deliver_ads.py --config <ads_config.json> [--dest <folder>]       (default dest = "dest" in the config)

Does, from the config's "delivery" list (number, id, file name, label; optional "carry" = an unchanged picture from an earlier round, optional "src" = the id of a regenerated file such as N06_Roommate_v2):
  1. copies carried-over pictures into <dir>/out/<id>.png;
  2. resizes every picture to the delivery size (1080x1350 for the 1024x1280 4:5 pictures; 1080x1080 for 1024x1024; 1080x1620 for 1024x1536; override with "delivery_size": "WxH" in the config)
     and writes <dest>/For Approval/<file>.png (clean names, no _v2; characters Windows forbids are removed);
  3. builds the numbered contact sheets: 4 columns, up to 8 pictures a sheet (so 15 pictures give 2 sheets), a big red number badge in the header strip (never on top of the picture), id and a short label;
  4. writes <dest>/PROMPTS_round<N>_exact.md, the full prompt of every picture, word for word (the tagged prompt of a regenerated picture when it exists);
  5. writes <dir>/delivery_key.json (number = id = file) so numbering stays stable across rounds.
It never deletes anything: files already in For Approval that are not part of this delivery are listed as STALE for you to move to an archive folder by hand.
Then YOU: view the sheets, send the sheets (render) and the prompts file (attach) to Soumil with SendUserFile when that tool is available in the session (otherwise give him the folder path), open the folder with Start-Process explorer.exe."""
import argparse, json, os, re, shutil, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import whole_ad

SIZES = {(1024, 1280): (1080, 1350), (1024, 1024): (1080, 1080), (1024, 1536): (1080, 1620), (1536, 1024): (1620, 1080)}


def clean_name(s):
    s = re.sub(r'[\\/:*?"<>|]+', '', s).strip().rstrip('.')
    return s


def delivery_size(cfg):
    if cfg.get('delivery_size'):
        w, h = cfg['delivery_size'].lower().split('x')
        return int(w), int(h)
    w, h = [int(x) for x in cfg.get('size', '1024x1280').lower().split('x')]
    return SIZES.get((w, h), (w, h))


def sheet(out, W, cols, items, outdir):
    HDR = 46
    H = int(W * 1.25)
    rows = (len(items) + cols - 1) // cols
    s = Image.new('RGB', (cols * W, rows * (H + HDR)), 'white')
    d = ImageDraw.Draw(s)
    fb = ImageFont.truetype('arialbd.ttf', 26)
    fs = ImageFont.truetype('arial.ttf', 17)
    for k, it in enumerate(items):
        im = Image.open('%s/out/%s.png' % (outdir, it.get('src', it['id']))).convert('RGB')
        im.thumbnail((W - 6, H - 6))
        x, y = (k % cols) * W, (k // cols) * (H + HDR)
        num = str(it['num'])
        d.ellipse((x + 6, y + 4, x + 6 + 38, y + 4 + 38), fill=(200, 25, 35))
        tw = d.textlength(num, font=fb)
        d.text((x + 6 + (38 - tw) / 2, y + 7), num, fill='white', font=fb)
        d.text((x + 52, y + 5), it.get('src', it['id']), fill='black', font=fs)
        d.text((x + 52, y + 24), it.get('label', ''), fill=(90, 90, 90), font=fs)
        s.paste(im, (x + 3, y + HDR))
    s.save(out, quality=90)
    print(out, s.size)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', required=True)
    ap.add_argument('--dest')
    a = ap.parse_args()
    cfg = whole_ad.load(a.config)
    d = cfg['_dir']
    dest = whole_ad.expand(a.dest or cfg['dest'])
    fa = dest + '/For Approval'
    os.makedirs(fa, exist_ok=True)
    items = sorted(cfg['delivery'], key=lambda x: x['num'])
    for it in items:
        if it.get('carry'):
            dst = '%s/out/%s.png' % (d, it.get('src', it['id']))
            if not os.path.exists(dst):
                shutil.copyfile(it['carry'], dst)
    missing = [it.get('src', it['id']) for it in items if not os.path.exists('%s/out/%s.png' % (d, it.get('src', it['id'])))]
    if missing:
        sys.exit('ERROR: these pictures do not exist in %s/out: %s (generate them, or set "carry" or "src" on the delivery entry)' % (d, missing))
    W, H = delivery_size(cfg)
    names = set()
    for it in items:
        name = clean_name(it['file'])
        names.add(name + '.png')
        im = Image.open('%s/out/%s.png' % (d, it.get('src', it['id']))).convert('RGB')
        if im.size != (W, H):
            im = im.resize((W, H), Image.LANCZOS)
        im.save('%s/%s.png' % (fa, name))
    print('delivered', len(items), 'pictures at %dx%d to' % (W, H), fa)
    for s in range(0, len(items), 8):
        chunk = items[s:s + 8]
        nm = 'Sheet %d - numbers %d to %d.jpg' % (s // 8 + 1, chunk[0]['num'], chunk[-1]['num'])
        names.add(nm)
        sheet('%s/%s' % (fa, nm), 470, 4, chunk, d)
    stale = [f for f in os.listdir(fa) if f not in names and f.lower().endswith(('.png', '.jpg'))]
    if stale:
        print('STALE (not part of this delivery, not deleted; move them to an archive folder by hand):', stale)
    refs = '; '.join('image %d = %s' % (k + 1, r['role']) for k, r in enumerate(cfg['refs']))
    lines = ['# %s round %s: the exact prompts, word for word' % (cfg.get('brand', ''), cfg.get('round', '')), '',
             'Model %s (edits endpoint), %s, quality %s, reference images on every call: %s. Each prompt below is the full text sent: reference roles + art direction + the concept + the avoid list. '
             'Pictures marked carried over were made in an earlier round (see that round\'s prompts file).' % (cfg.get('model', 'gpt-image-2.5-sunburst'), cfg.get('size', '1024x1280'), cfg.get('quality', 'high'), refs), '']
    cs = {c['id']: c for c in cfg['concepts']}
    for it in items:
        src = it.get('src', it['id'])
        head = '## %d  %s  (%s)' % (it['num'], src, it['file'])
        cands = ['%s/p/%s.txt' % (d, src), '%s/p/%s.txt' % (d, it['id'])]
        p = next((c for c in cands if os.path.exists(c)), None)
        if p:
            lines += [head, '', open(p, encoding='utf-8').read(), '']
        elif it['id'] in cs and not it.get('carry'):
            lines += [head, '', whole_ad.assemble(cfg, cs[it['id']]), '']
        else:
            lines += [head, '', 'Carried over from an earlier round.', '']
    pf = '%s/PROMPTS_round%s_exact.md' % (dest, cfg.get('round', ''))
    open(pf, 'w', encoding='utf-8').write('\n'.join(lines))
    json.dump([[it['num'], it['id'], it['file'], it.get('label', '')] for it in items], open(d + '/delivery_key.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('prompts file:', pf)
    print('NEXT: view the sheets, send the sheets and the prompts file (SendUserFile), open the folder.')


if __name__ == '__main__':
    main()
