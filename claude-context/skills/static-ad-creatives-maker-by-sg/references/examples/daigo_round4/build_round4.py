"""Daigo round 4 (10 Oct 2026, evening): the image model draws the WHOLE ad (scene, real pouch, branded sachets, headline, badges) from the real product references, with the new Hinglish and English lines.
Same recipe as round 3 (graphics approved in spirit by Soumil); the lines come from the screened copy table; the picture fixes come from the slang screen.
  python build_round4.py prompts [ID ...]   -> p\\<ID>.txt (the exact prompt, saved so it can be shown)
  python build_round4.py gen [ID ...] [--tag _vN]   -> gpt-image-2.5-sunburst edits endpoint with the reference images, 1024x1280 (4:5)
The concept bodies live in concepts_round4.py."""
import json, os, sys, subprocess
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, 'C:/cca/daigo/round4')
from concepts_round4 import C

R4 = 'C:/cca/daigo/round4'
R3 = 'C:/cca/daigo/round3'
SK = 'C:/Users/soumi/.claude/skills/static-ad-creatives-maker-by-sg/scripts'
POUCH = R3 + '/pouch_clean_ai.png'      # the real pouch with the badge, seal and icon row removed (audit C38)
SACHET = R3 + '/sachet_ref.png'         # the branded stick-pack sachet (canonical, made from the pouch)
for d in ('p', 'out'):
    os.makedirs(R4 + '/' + d, exist_ok=True)

ROLE_REFS = ("REFERENCE IMAGES: image 1 is the REAL Daigo stand-up pouch (use it as the product, keep it recognisable and correctly spelled); "
             "image 2 is the REAL Daigo stick-pack sachets. "
             "Reproduce the pouch and the sachets faithfully from these references: royal-blue panel, green lower band, the white italic 'daigo' wordmark with 'dairy on the go', 'Instant Chaas Premix', 'Classic Masala' on the pouch, the milk-splash glass illustration and the spice bowl. "
             "Sachets are SLIM VERTICAL STICK PACKS with crimped silver foil ends and the same blue printed front with the daigo wordmark: never plain, never square, never a small square packet. "
             "Do not add any badge, seal, icon, claim or extra wording to the pouch or the sachets beyond what the references show. Pouch and sachets are sharp, large enough to read, lit by the same light as the scene, with contact shadows and believable perspective, physically part of the scene (standing, leaning, held or resting on surfaces), never floating pasted-on cut-outs.")

ART = ("Create a FINISHED professional Meta feed advertisement, 4:5 portrait, art directed like a top D2C brand poster, in the construction style of the best static ads: ONE clear focal point; "
       "a disciplined palette of at most three brand hues (royal blue #204898, fresh green #84B355, warm yellow #F2C41E) plus white and the product's own colours; the background is a designed colour field or a built studio set, not a casual snapshot; "
       "clean soft studio lighting with soft believable shadows, specular highlights and condensation; three-level type hierarchy (a huge headline, one small supporting line, optional tiny badge); the typography is part of the design (it overlaps, wraps or sits behind elements where that helps) and carries one treatment such as a highlight bar, an underline swoosh or a two-colour split; "
       "the headline and the picture tell ONE story and the product takes part in that story; generous margins, all text and key objects inside the central 84% of the frame, nothing important touching an edge. "
       "Every piece of text must be spelled EXACTLY as given, letter for letter, cleanly rendered and aligned. No other text, no watermark, no fake UI.")

NEG = ("Avoid: a pasted-on look, flat cut-out products, a casual phone-snapshot look, empty unused space, plain unbranded sachets, square packets, stock-photo smiles, extra logos, invented claims, health claims, any text that was not specified, garbled lettering, extra fingers, "
       "readable text on any background object (book spines, signboards, labels, screens) other than the text specified, white powder clouds, white liquid splashes or sprays, clinking glasses, sachets tucked into pockets, unlabelled clear bottles, the logo of any real company or of the railways.")


def assemble(i):
    return ' '.join([ROLE_REFS, ART, C[i]['body'], NEG])


def write_prompts(ids):
    for i in (ids or C):
        open(R4 + '/p/%s.txt' % i, 'w', encoding='utf-8').write(assemble(i))
    print('prompts written:', ids or list(C))


def gen(ids, tag=''):
    ids = ids or list(C)

    def one(i):
        c = C[i]
        refs = [POUCH, SACHET] + ([c['style']] if c.get('style') else [])
        cmd = ['python', SK + '/gen_image.py', '--prompt-file', R4 + '/p/%s.txt' % i, '--out', R4 + '/out/%s%s.png' % (i, tag), '--size', c.get('size', '1024x1280'), '--tag', 'daigo_r4_' + i + tag, '--model', 'gpt-image-2.5-sunburst']
        for r in refs:
            cmd += ['--ref', r]
        r = subprocess.run(cmd, capture_output=True, text=True)
        return i, (r.stdout + r.stderr).strip()[-160:]
    with ThreadPoolExecutor(5) as ex:
        for i, msg in ex.map(one, ids):
            print(i, '->', msg)


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    args = sys.argv[2:]
    tag = ''
    if '--tag' in args:
        k = args.index('--tag'); tag = args[k + 1]; args = args[:k] + args[k + 2:]
    {'prompts': lambda: write_prompts(args), 'gen': lambda: gen(args, tag)}[cmd]()
