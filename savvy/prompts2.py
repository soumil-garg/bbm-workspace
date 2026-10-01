import json, prompts as pr
from prompts import P_, K, C, D, O
P={}
P['X1_A_StrapSplit']=P_(
 f'Warm blush-cream ({C}) background. Top 28%: headline in huge heavy near-black sans, two centred lines: "STRAPS SLIPPING?" / "GLUE THEM IN PLACE." '
 'Middle 50%: two equal square photo panels side by side with a thin gap. Left panel: close crop of an Indian woman\'s shoulder in a satin noodle-strap top with the strap slipped down off the shoulder, no face. Right panel: the same shoulder with the strap sitting neatly in place. Between the panels a small arrow. '
 f'Bottom 14%: a rounded pink ({K}) pill with near-black text "Savvy Body Glue sticks clothes to skin." At the far right of the middle row nothing else. One small upright Savvy tube in the bottom-left corner. That is ALL the text.', 'H', real=True)
P['X2_P_WhatIs']=P_(
 f'Warm off-white ({O}) background, strict clean grid. Top 30%: headline in huge heavy near-black sans, three centred lines: "WHAT IS BODY GLUE?" / "IT STICKS YOUR CLOTHES" / "TO YOUR SKIN." '
 'Middle: three equal rounded panels in a row, each a simple flat illustration: panel 1 a hand drawing a thin line along the inside edge of a blouse neckline, panel 2 a small clock, panel 3 a hand pressing the neckline against the skin. Under the panels three short labels in order: "1 Thin line" / "2 Wait 30 sec" / "3 Press". '
 f'Bottom: one upright Savvy tube and small text "Savvy Body Glue". Accent colour {K} only on the panel outlines. That is ALL the text.', 'P')
P['X3_F_Neckline']=P_(
 'Left 55%: a real Indian woman about 28 at a wedding reception, in a saree blouse, glancing down with a mildly annoyed look while one hand holds her neckline in place, warm blurred fairy lights behind, modest framing from the waist up. '
 f'Right 45% on a clean warm blush-cream ({C}) panel: headline in huge heavy near-black sans, three stacked lines: "NECKLINE" / "WON\'T STAY?" / "USE BODY GLUE." Below, small near-black text: "It sticks clothes to your skin." At the bottom of the panel one upright Savvy tube, large and legible. That is ALL the text.', 'F', real=True)
P['X4_A_Macro']=P_(
 'Close-up editorial photograph in soft window light: the edge of a mustard cotton kurti neckline pressed flat against an Indian woman\'s collarbone skin, a thin clear line of glue visible along the inside edge where fabric meets skin, fabric lying neatly. No face. A Savvy tube rests in the bottom-right corner, sharp and legible. '
 f'Headline at the top in large heavy near-black sans, two lines: "GLUE THAT STICKS" / "CLOTHES TO SKIN." Small near-black text beneath: "Savvy Body Glue. Up to 8 hours." That is ALL the text.', 'A', real=True)
P['X5_N_Notes']=P_(
 f'A flat note page filling the whole canvas, cream paper colour ({C}) with faint horizontal lines, plain default sans-serif typography, no app chrome. Large bold black title: "What is body glue?" Then regular-weight lines, one under the other: "A skin-safe glue that sticks your clothes to your skin." / "Necklines. Straps. Drapes." / "Thin line. Wait 30 seconds. Press." '
 'Below the text a small rounded-corner photo inserted into the note showing one upright Savvy tube on a plain white shelf. That is ALL the text.', 'N')
P['X6_U_Sign']=P_(
 'A flat piece of brown cardboard leaning on a wall, photographed with harsh phone flash, slightly crooked. Big messy black marker handwriting: "GLUE FOR YOUR CLOTHES." in two lines, and smaller below: "Sticks necklines and straps to your skin. No pins." One Savvy tube stands upright in front at the bottom right, sharp and legible. No other writing, no doodles.', 'U')
P['X7_P_NoPins']=P_(
 f'Solid soft pink ({K}) background. Top 28%: headline in huge heavy near-black rounded sans, two centred lines: "NO PINS. NO TAPE." / "JUST GLUE." '
 'Middle: three equal items in a row with generous space: a silver safety pin with a red cross over it, a strip of clear tape with a red cross over it, and one upright Savvy tube with a green tick. '
 f'Bottom: a rounded cream ({C}) pill with near-black text "Body glue sticks clothes to skin." That is ALL the text.', 'M')
out={'PRE':pr.PRE,'REAL':pr.REAL,'SUF':pr.SUF,'LEAN':pr.LEAN,'SYS':pr.SYS,'items':{}}
for k,v in P.items():
    s=v[len(pr.PRE):]; real=s.startswith(pr.REAL)
    if real: s=s[len(pr.REAL):]
    s=s[len("1:1 static ad creative, 1080x1080. "):]; s=s[:-len(pr.SUF)]; s=s[:-len(pr.LEAN)]
    sk=[a for a,b in pr.SYS.items() if s.endswith(b)][0]; s=s[:-len(pr.SYS[sk])]
    out['items'][k]={'b':s,'s':sk,'r':int(real)}
j=json.dumps(out['items'],ensure_ascii=False,separators=(',',':'))
open('items2.json','w',encoding='utf-8').write(j)
print(len(j)); print(j); print({k:len(v) for k,v in P.items()})
