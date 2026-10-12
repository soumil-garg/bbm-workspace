"""Daigo round 2 build (2026-10-10). Voice first: Hinglish headlines chosen after an independent critic pass (round2\\critic_output.md), claims only from copy_v2.json register R1 to R14.
Look built from what Soumil approves in the Swipe Desk and liked in September: loud saturated colour, one big headline, the pack big, real people, a glass of chaas.
The model draws SCENES (people, glass, props, and for the lettered arm the headline as part of the poster). Code places the REAL pack crop, the logo, stickers and, for the typed arm, every word.
  python build_round2.py prompts [ID ...]   -> p\\<ID>.txt
  python build_round2.py gen [ID ...]       -> scenes through gen_image.py (parallel)
  python build_round2.py render [ID ...]    -> layouts\\<ID>.json and img\\<ID>.png through render_ad.py
"""
import json, os, re, sys, subprocess, random
from concurrent.futures import ThreadPoolExecutor

ROOT = 'C:/cca/daigo'
R2 = ROOT + '/round2'
SK = 'C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg/scripts'
KITP = ROOT + '/kit/brand-kit.json'
KIT = json.load(open(KITP, encoding='utf-8'))
PAL = {**KIT['colors'], **KIT['flex']}
PACK = ROOT + '/assets/pack_masala_top_cut_clean.png'   # the real pack crop with the "10's" badge painted out (it can read as ready in 10 seconds, audit C01 and C38)
LB = ROOT + '/ref/logo_new_01.png'   # transparent wordmark for light backgrounds
LW = ROOT + '/ref/logo_new_02.png'   # white wordmark on its own blue block
FONTS = ['Baloo 2', 'Poppins', 'Caveat']
SIZE = [1080, 1080]
for d in ('p', 'img', 'layouts'):
    os.makedirs(R2 + '/' + d, exist_ok=True)

SUF = (" [NO TEXT] Absolutely no text, letters, numbers, logos, brand names, labels or watermarks anywhere in the image; every foil sachet, bottle, box and tumbler is completely plain."
       " [NO PLATFORM CHROME] A standalone photograph only: no phone frame, no status bar, no captions."
       " [PEOPLE] Natural Indian faces and skin, believable hands with five fingers each, no airbrushed look."
       " [EDGE-SAFE] Keep every important object inside the central 84% of the frame.")
SUF_LETTERED = (" [NO OTHER TEXT] Apart from the headline specified above, there is no other text, logo, brand name, number or watermark anywhere; every foil sachet, bottle and tumbler is completely plain."
                " [PEOPLE] Natural Indian faces and skin, believable hands with five fingers each, no airbrushed look."
                " [EDGE-SAFE] Keep the headline and every important object inside the central 84% of the frame; spell the headline exactly as given, letter for letter.")

# scene id -> (size, prompt body). Text-free plates for the typed arm. The pack, logo, stickers and words are added by code.
SCENES = {
    'S1_Hostel': ('1024x1024',
        "A real photograph, square, shot on a good phone in an Indian college hostel room in the evening. A young Indian man of about 21 in a grey hoodie sits cross-legged on a bunk bed, holding a steel tumbler of pale creamy chaas "
        "toward the camera with a smug, playful grin; in his other hand a torn plain silver foil sachet. Behind him a small lived-in hostel room: warm fairy lights, a study table with books and a laptop, a small closed mini-fridge, a window. "
        "Warm tungsten light, shallow depth of field, slight grain. The top 32% of the frame is calm, only a plain pale wall and a few fairy lights, no objects. The bottom-right corner (the right 36% and bottom 26%) is just an empty blanket surface."),
    'S2_Train': ('1024x1024',
        "A candid documentary photograph, square. Two friends in their mid-20s sit facing each other across a table by the window of a modern Indian intercity train chair car, bright daylight and green countryside blurred outside. "
        "The man on the left tears the notch of a plain silver foil sachet above a clear plastic bottle held in his other hand while the woman on the right laughs, holding a steel glass. A small snack box on the table. "
        "The top 30% of the frame is only the window light and soft blur, no objects. The bottom-right corner (right 36%, bottom 26%) is an empty table surface."),
    'S3_PGKitchen': ('1024x1024',
        "A real photograph with a touch of humour, square. A narrow Indian PG (paying guest) kitchenette in bright tube-light daylight: a steel sink piled with dirty dishes and a used Indian mixer-grinder jar (clear plastic jar with a steel blade base, white curd residue inside) sitting in the sink; "
        "a single-burner gas stove on the counter. A young Indian woman in her late 20s in a casual kurta top stands at the counter, completely calm, shaking a clear plastic shaker bottle of pale chaas with a small satisfied smile, ignoring the mess. "
        "The top 30% of the frame is plain tiled wall, nothing on it. The bottom-right corner (right 36%, bottom 24%) is empty counter."),
    'S4_Steps': ('1024x1024',
        "A dynamic studio photograph, square: two Indian hands tear the notch of a plain silver foil sachet above the open mouth of a clear plastic shaker bottle, a stream of fine cream-white powder with tiny green flecks falling into the bottle in mid-air; "
        "a few powder particles floating. Flat saturated royal blue seamless backdrop (colour #204898), crisp highlights, hard rim light, high-speed look. The top 38% of the frame is empty blue; hands and bottle are centred in the lower middle of the frame."),
    'S5_Bag': ('1024x1024',
        "A bright studio photograph, square, on a seamless flat fresh-green backdrop (colour #84B355) with a matching green surface. A canvas backpack in deep navy blue stands upright at the lower left, its front pocket open with a cluster of plain silver foil sachets tumbling out, "
        "a steel tumbler of pale creamy chaas beside it. Hard, punchy light with a crisp shadow. The top 46% of the frame and the right 36% are empty green backdrop."),
    'S6_Glass': ('1024x1024',
        "A dramatic product photograph, square: one tall clear glass of pale creamy chaas with light condensation, tiny green herb flecks and a sprinkle of roasted-cumin brown specks on the surface, standing on a glossy deep blue surface against a deep navy backdrop (colour #1C2F6B) "
        "with a soft pool of light behind it, strong rim light. The glass stands in the left third of the frame, slightly low. The top 40% and the right 48% of the frame are empty navy backdrop."),
    'S7_Rooftop': ('1024x1024',
        "A cinematic photograph, square. A young Indian woman of about 25 sits on a plastic chair on the terrace of an old PG building at dusk, knees up, holding a steel tumbler of pale chaas in both hands and looking toward a softly blurred city skyline with warm lights, a quiet wistful smile. "
        "A torn plain foil sachet on the parapet beside her. Golden-hour rim light, shallow depth of field. The top 32% of the frame is only glowing sky, no objects. The bottom-right corner (right 36%, bottom 24%) is parapet and shadow only."),
    'S10_GlassYellow': ('1024x1024',
        "A bright studio product photograph, square, on a seamless flat saturated yellow backdrop (colour #F2C41E) with a matching yellow surface. One tall clear glass of pale creamy chaas with light condensation, tiny green herb flecks and a sprinkle of roasted-cumin brown specks on top stands at the lower left third, "
        "with a few cumin seeds scattered on the surface beside it. Hard punchy light and a crisp soft shadow. The top 45% and the right 45% of the frame are empty yellow backdrop."),
    'S12_Note': ('1024x1024',
        "A close-up phone photograph, square, of a steel tumbler holding pale creamy chaas next to a small stack of plain silver foil sachets on a metal shelf in an Indian hostel room. A strip of beige masking tape is stuck across the front of the tumbler, "
        "with handwriting in thick black marker, in two lines of block capitals, slightly uneven like real handwriting, easy to read, exactly: ROOM 204 KI CHAAS. then on the second line: HAATH MAT LAGANA. "
        "Warm light, shallow depth of field, a cupboard softly blurred behind. The tumbler stands in the left half of the frame and the bottom-right corner (right 36%, bottom 24%) is empty shelf."),
    'S13_Office': ('1024x1024',
        "A candid photograph, square, in a bright modern Indian office pantry. A young Indian woman in her late 20s in a smart-casual shirt with a lanyard stands at the counter holding a steel glass of pale creamy chaas, laughing with a male colleague who holds his own steel glass; "
        "a clear plastic bottle and two plain foil sachets on the counter, a laptop and notebooks on a standing table behind them, daylight from large windows. The people stand in the lower two thirds of the frame."),
    'S14_RoadTrip': ('1024x1024',
        "A candid photograph, square, at a highway dhaba parking area in bright daylight. A young Indian couple in their late 20s stand beside the open boot of a hatchback, laughing; he holds a steel glass of pale creamy chaas, she holds a clear plastic bottle; "
        "backpacks in the boot, a charpai and a painted wall softly blurred behind, blue sky. The people stand in the lower two thirds of the frame."),
    'S9_Roommates': ('1024x1024',
        "A candid photograph, square. Two young Indian roommates, men in their early 20s, in a hostel room clink steel tumblers of pale chaas and laugh; a few empty plain foil sachets lie on the study table between them; bunk beds and a window behind, warm light. "
        "The top 30% of the frame is plain wall only. The bottom-right corner (right 36%, bottom 24%) is empty tabletop."),
}


LETTERED = {'L1_Hostel': ('S1_Hostel', 'C1'), 'L2_Train': ('S2_Train', 'C2'), 'L7_Rooftop': ('S7_Rooftop', 'C7'), 'L13_Office': ('S13_Office', 'C13'), 'L14_Road': ('S14_RoadTrip', 'C14')}   # lettered arm: the model draws the headline as part of the poster


def lettered_prompt(sid, cid):
    body = SCENES[sid][1]
    lines = json.load(open(R2 + '/copy_r2.json', encoding='utf-8'))[cid]['h']
    up = [l.upper() for l in lines]
    cols = ['white', 'bright yellow (#F2C41E)']
    spec = ' '.join('Line %d: "%s" in %s.' % (k + 1, t, cols[min(k, 1)]) for k, t in enumerate(up))
    extra = (" POSTER LETTERING: this photograph is a finished static ad. Set the headline in huge heavy condensed all-caps sans-serif lettering (like a sports or movie poster, tight letter spacing) across the top of the frame, "
             "exactly %d lines, spelled letter for letter. %s A soft dark gradient sits behind the letters for legibility. Compose the people lower in the frame so the top 30%% is free for the lettering; the letters must never cover a face." % (len(up), spec))
    return body + extra + SUF_LETTERED


def write_prompts(ids):
    for lid, (sid, cid) in LETTERED.items():
        if not ids or lid in ids:
            open(R2 + '/p/%s.txt' % lid, 'w', encoding='utf-8').write(lettered_prompt(sid, cid))
    for i, (size, body) in SCENES.items():
        if ids and i not in ids:
            continue
        open(R2 + '/p/%s.txt' % i, 'w', encoding='utf-8').write(body + (SUF_LETTERED if i.startswith('S12') else SUF))
    print('prompts written')


def gen(ids):
    ids = ids or list(SCENES)

    def one(i):
        size = SCENES[LETTERED[i][0]][0] if i in LETTERED else SCENES[i][0]
        out = R2 + '/img/scene_%s.png' % i
        cmd = ['python', SK + '/gen_image.py', '--prompt-file', R2 + '/p/%s.txt' % i, '--out', out, '--size', size, '--tag', 'daigo_r2_' + i, '--model', 'gpt-image-2.5-sunburst']
        r = subprocess.run(cmd, capture_output=True, text=True)
        return i, (r.stdout + r.stderr).strip()[-160:]
    with ThreadPoolExecutor(6) as ex:
        for i, msg in ex.map(one, ids):
            print(i, '->', msg)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    ids = sys.argv[2:]
    {'prompts': lambda: write_prompts(ids), 'gen': lambda: gen(ids)}[cmd]()
