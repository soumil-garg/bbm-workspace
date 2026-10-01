import json, prompts as pr
from prompts import P_, K, C, D, O
P = {}
P['X8_H_Gaping'] = P_(
 f'Warm blush-cream ({C}) background. Top 28%: headline in huge heavy near-black sans, two centred lines: "NECKLINE GAPING?" / "BODY GLUE KEEPS IT FLAT." '
 'Middle 50%: two equal square photo panels side by side with a thin gap. Left panel: close crop of a collared shirt neckline on an Indian woman, no face, the neckline gapping open and sagging away from the collarbone. Right panel: the same neckline lying flat and neat against the collarbone. A small arrow between the panels. '
 f'Bottom 14%: a rounded pink ({K}) pill with near-black text "It sticks clothes to your skin." One small upright Savvy tube in the bottom-left corner. That is ALL the text.', 'H', real=True)
P['X9_A_Drape'] = P_(
 'Editorial photograph in warm window light: an Indian woman in a silk saree, cropped from shoulder to waist with no face, a hand gently pressing the saree drape at her shoulder into place so it lies smooth, a Savvy tube held in the other hand, sharp and legible. '
 f'Headline in the empty space at the top in large heavy near-black sans, two lines: "DRAPE SLIPPING?" / "USE BODY GLUE." Small near-black text beneath: "It sticks clothes to your skin." That is ALL the text.', 'A', real=True)
P['X10_P_ThreeFixes'] = P_(
 f'Warm off-white ({O}) background, strict clean grid. Top 26%: headline in huge heavy near-black sans, two centred lines: "WHAT DOES" / "BODY GLUE FIX?" '
 'Middle: three equal rounded photo panels in a row, each a close crop with no faces: panel 1 a satin noodle strap slipping off a shoulder, panel 2 a blouse neckline gaping open, panel 3 a saree drape sliding off a shoulder. Under the panels three short labels in order: "Slipping straps" / "Gaping necklines" / "Sliding drapes". '
 f'Bottom: one upright Savvy tube and small near-black text "Body glue sticks clothes to your skin." That is ALL the text.', 'P', real=True)
P['X11_A_HowItWorks'] = P_(
 f'Warm blush-cream ({C}) background. Top 24%: headline in huge heavy near-black sans, two centred lines: "HOW BODY GLUE WORKS" / "IT STICKS CLOTHES TO SKIN." '
 'Middle: three equal square real photographs in a row with thin gaps: photo 1 a hand drawing a thin clear line of glue along the inside edge of a blouse neckline from a Savvy tube, photo 2 a close-up of a wristwatch face showing about half a minute, photo 3 a hand pressing the neckline gently against the collarbone skin. No faces. Under the photos three short labels in order: "1 Thin line" / "2 Wait 30 seconds" / "3 Press". '
 'Bottom: one small upright Savvy tube. That is ALL the text.', 'A', real=True)
P['X12_N_Search'] = P_(
 f'A flat screen-like image filling the canvas on a {O} background, plain default UI typography, no app chrome or logos. Top: a white rounded search bar with a magnifier icon containing the text "how to stop blouse neckline from slipping". '
 'Below it a large white rounded answer card with a bold title "Body glue", under it the text "A skin-safe glue that sticks your clothes to your skin.", a small rounded photo of one upright Savvy tube on the left, and the small text "Savvy Body Glue". That is ALL the text.', 'N')
P['X13_P_Compare'] = P_(
 f'Warm off-white ({O}) background, strict clean grid. Top 22%: headline in huge heavy near-black sans, two centred lines: "SAFETY PIN. TAPE." / "OR BODY GLUE?" '
 'Middle: three equal columns. Column 1 a silver safety pin with the caption "Pins fabric to fabric." Column 2 a strip of clear double-sided tape with the caption "A sticky strip under the fabric." Column 3 one upright Savvy tube with the caption "A thin line that holds fabric to skin." and a small pink circle highlight behind it. '
 'Captions in small near-black sans, equal size. That is ALL the text.', 'P')
P['X14_F_Mirror'] = P_(
 'A real Indian woman about 27 standing at a bedroom mirror in a satin top, framed from the shoulders down plus her reflection, smoothing the neckline flat against her collarbone with one hand while holding a Savvy tube in the other, calm and pleased, soft morning window light, modest framing. '
 f'Headline in the empty space at the top in large heavy near-black sans, two lines: "BODY GLUE HOLDS YOUR" / "CLOTHES TO YOUR SKIN." Small near-black text beneath: "Thin line. Wait 30 seconds. Press." That is ALL the text.', 'F', real=True)

out = {}
for k, v in P.items():
    s = v[len(pr.PRE):]
    real = s.startswith(pr.REAL)
    if real:
        s = s[len(pr.REAL):]
    s = s[len("1:1 static ad creative, 1080x1080. "):]
    s = s[:-len(pr.SUF)]
    s = s[:-len(pr.LEAN)]
    sk = [a for a, b in pr.SYS.items() if s.endswith(b)][0]
    s = s[:-len(pr.SYS[sk])]
    out[k] = {'b': s, 's': sk, 'r': int(real)}
j = json.dumps(out, ensure_ascii=False, separators=(',', ':'))
open(r'C:\cca\savvy\items3.json', 'w', encoding='utf-8').write(j)
print(len(j))
print(j)
print({k: len(v) for k, v in P.items()})
