"""Daigo round 4 delivery: picks the final image per number, upscales to 1080x1350, writes Daigo Ads\\Round 4\\For Approval, the numbered sheets and PROMPTS_round4_exact.md.
Numbers 11 and 13 are the unchanged round 3 pictures (their lines did not change and passed the screen); every other number is a round 4 picture.
  python deliver_round4.py            -> uses KEY below (edit KEY when a picture is replaced by a regeneration)"""
import os, sys, shutil, subprocess, json, glob
from PIL import Image

R4 = 'C:/cca/daigo/round4'
R3 = 'C:/cca/daigo/round3'
DEST = 'C:/Users/soumi/OneDrive/Desktop/Daigo Ads/Round 4'
FA = DEST + '/For Approval'

# number, image id in round4/out, delivery file name, short label for the sheet
KEY = [
    (1, 'N01_Waitlist', '01_Waitlisted_Chaas_is_confirmed', 'ticket pun, yellow field'),
    (2, 'N02_NoStep4', '02_There_is_no_step_4', 'three steps, no step 4'),
    (3, 'N03_Under30', '03_Under_Rs_30_a_glass', 'price per glass, blue studio'),
    (4, 'N04_Hostel', '04_Dahi_in_a_hostel_Cute', 'smug student, cream field'),
    (5, 'N05_PG', '05_PG_mein_mixer_kaun_dhoyega', 'dirty mixer vs sachet, split'),
    (6, 'N06_Roommate', '06_Roommate_ye_mera_hai', 'taped tumbler, still life'),
    (7, 'N07_Email', '07_Couldve_been_an_email_Chaas_couldnt', 'desk flat-lay, one tumbler'),
    (8, 'N08_Packed', '08_Packed_playlist_snacks_chaas', 'packed boot, road trip'),
    (9, 'N09_Roommates', '09_Roommates_exist_Get_20', 'offer: 20-pack, hands on the stash'),
    (10, 'N10_Chat', '10_Mummy_chat', 'native: chat on a phone'),
    (11, 'N11_GharDoor', '11_Ghar_door_Chaas_paas', 'window at dusk (round 3, unchanged)'),
    (12, 'N12_Mess', '12_Mess_mein_dal_Room_mein_chaas', 'dull mess thali vs chaas'),
    (13, 'N13_Bag', '13_Bag_mein_chaas_ki_dukaan', 'bag of sachets (round 3, unchanged)'),
    (14, 'N14_Maths', '14_The_easiest_maths', 'new: sachet + water = chaas'),
    (15, 'N15_Shout', '15_Soooo_much_chaas', 'new: loud shout over the pile'),
]

# the unchanged round 3 pictures are copied into round4/out under their round 4 ids
for new, old in (('N11_GharDoor', 'L_GharDoor'), ('N13_Bag', 'N_Bag_v2')):
    dst = R4 + '/out/%s.png' % new
    if not os.path.exists(dst):
        shutil.copyfile(R3 + '/out/%s.png' % old, dst)

os.makedirs(FA, exist_ok=True)
for n, i, name, label in KEY:
    im = Image.open(R4 + '/out/%s.png' % i).convert('RGB')
    im = im.resize((1080, 1350), Image.LANCZOS)
    im.save(FA + '/%s.png' % name)
print('delivered', len(KEY), 'pictures to', FA)


def sheet(out, W, cols, items):
    from PIL import ImageDraw, ImageFont
    HDR = 46
    rows = (len(items) + cols - 1) // cols
    s = Image.new('RGB', (cols * W, rows * (int(W * 1.25) + HDR)), 'white')
    d = ImageDraw.Draw(s)
    fb = ImageFont.truetype('arialbd.ttf', 26)
    fs = ImageFont.truetype('arial.ttf', 17)
    for k, (n, i, name, label) in enumerate(items):
        im = Image.open(R4 + '/out/%s.png' % i).convert('RGB')
        im.thumbnail((W - 6, int(W * 1.25) - 6))
        x, y = (k % cols) * W, (k // cols) * (int(W * 1.25) + HDR)
        num = str(n)
        d.ellipse((x + 6, y + 4, x + 6 + 38, y + 4 + 38), fill=(200, 25, 35))
        tw = d.textlength(num, font=fb)
        d.text((x + 6 + (38 - tw) / 2, y + 7), num, fill='white', font=fb)
        d.text((x + 52, y + 5), i, fill='black', font=fs)
        d.text((x + 52, y + 24), label, fill=(90, 90, 90), font=fs)
        s.paste(im, (x + 3, y + HDR))
    s.save(out, quality=90)
    print(out, s.size)


sheet(FA + '/Sheet 1 - numbers 1 to 8.jpg', 470, 4, KEY[:8])
sheet(FA + '/Sheet 2 - numbers 9 to 15.jpg', 470, 4, KEY[8:])

# the exact prompts
ids = [i for n, i, name, label in KEY if os.path.exists(R4 + '/p/%s.txt' % i)]
lines = ['# Daigo round 4: the exact prompts, word for word', '',
         'Model gpt-image-2.5-sunburst (edits endpoint), 1024x1280, quality high, two reference images on every call: image 1 = the real pouch with the badge, seal and icon row removed (round3/pouch_clean_ai.png), image 2 = the branded stick-pack sachet (round3/sachet_ref.png). '
         'Each prompt below is the full text sent: reference roles + art direction + the concept + the avoid list. Numbers 11 and 13 are the unchanged round 3 pictures (see round 3 prompts). Regenerated pictures are listed at the end.', '']
for n, i, name, label in KEY:
    p = R4 + '/p/%s.txt' % i
    if os.path.exists(p):
        lines += ['## %d  %s  (%s)' % (n, i, name), '', open(p, encoding='utf-8').read(), '']
open(DEST + '/PROMPTS_round4_exact.md', 'w', encoding='utf-8').write('\n'.join(lines))
print('prompts file written for', len(ids), 'pictures')
