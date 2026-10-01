"""Savvy Body Glue prompt builder. Run: python prompts.py -> writes p\<ID>.txt"""
import os

WORK = r'C:\cca\savvy'
BRAND = {
    'name': 'Savvy Body Glue',
    'products': {
        'hero': "a slim matte deep forest-green squeeze tube (about #1F4A34): a flat ridged crimped seal at one end, a short cylindrical screw cap at the other end, and the soft pink (#E9A2B2) bubbly hand-lettered wordmark SAVVY running vertically up the front. No other text on the tube",
    },
    'cream': '#F4E6E1', 'dark': '#141715', 'pink': '#E9A2B2', 'offwhite': '#F6EDE9',
    'locale': 'Indian subject, natural Indian skin tone',
}

PRE = ("Generate an image. The attached photo is the exact product reference for the brand " + BRAND['name'] + ". "
       + " ".join(f"{k}: {v}." for k, v in BRAND['products'].items()) +
       " Reproduce every tube exactly as in the reference: same green, same shape, same pink wordmark and layout. "
       "Show ONLY the tube itself: no flower, shadows, props or backgrounds from the reference. "
       "Do not add any text to the tube. Do not invent products or brands. ")

SUF = (" [NO PLATFORM CHROME] Standalone ad creative only. No phone status bar, device frame, Sponsored label, like counts or app buttons unless explicitly described."
       " [EDGE-SAFE] All text and key objects within the central 84% of the canvas, about 8% padding from every edge."
       " [TEXT FIDELITY] Render exactly the words in double quotes, spelled exactly, with exactly these prices; no extra words, numbers, claims or logos anywhere.")

REAL = (" PHOTOREALISM: full-frame camera, 35-50mm lens, natural skin texture with pores, real fabric creases, true-to-life light, slight grain; "
        "a real unretouched photograph, not CGI. " + BRAND['locale'] + ". Correct anatomy: exactly two arms and two hands, five fingers each. "
        "Modest, tasteful framing: fully clothed, no cleavage emphasis, no bare midriff, nothing revealing. ")

SYS = {
 'M': " [DESIGN SYSTEM: MINIMAL SWISS] Premium, uncluttered. The headline is the dominant element, at least 3x larger than any other text. At least 40% empty space. Single centre axis. Soft even studio light, heavy modern rounded-geometric sans-serif.",
 'T': " [DESIGN SYSTEM: BOLD TYPOGRAPHY] Type is the hero, heavy condensed sans-serif, tight leading, flush left. Products small. Two colours plus the accent. No decorations.",
 'N': " [DESIGN SYSTEM: NATIVE LO-FI] Looks like something an ordinary person made on their phone, not an advertisement: plain default phone typography, no brand styling, no polish; blends into a social feed.",
 'F': " [DESIGN SYSTEM: FACE AND GAZE] A real person's face draws attention first; their eye-line points at the product or the text, not at the camera. Product large and legible. Headline in clean empty space away from the face.",
 'H': " [DESIGN SYSTEM: PRODUCT HERO CONTRAST] One product is isolated and different from everything else so it pops. Single clean light source, soft deep shadow, museum-like emptiness. Minimal text.",
 'P': " [DESIGN SYSTEM: PROOF AND DATA] Clean information design; the numbers are the hero. Strict grid, precise alignment, generous spacing, near-black type on warm off-white, accent only on the pay-price.",
 'A': " [DESIGN SYSTEM: RICH ART DIRECTION] Editorial magazine-quality photograph, a fully styled real scene with warm natural light and depth. Richness lives in the image, not the text: one headline, one message.",
 'U': " [DESIGN SYSTEM: DELIBERATELY UGLY] Intentionally amateur and scrappy, like a rushed homemade post: flat phone flash, slightly crooked framing, marker or pen handwriting. Unpolished, but the headline must be large and perfectly legible.",
}
LEAN = (" [LEAN LAYOUT] Keep it airy: at least 40% empty background, no extra lines, footers, icons or decorations. Only the text listed.")


def P_(body, system, real=False, lean=True):
    return PRE + (REAL if real else "") + "1:1 static ad creative, 1080x1080. " + body + SYS[system] + (LEAN if lean else "") + SUF


C, D, K, O = BRAND['cream'], BRAND['dark'], BRAND['pink'], BRAND['offwhite']
P = {}

# ---------- T1: tape came off in 10 minutes? ----------
P['T1_H_Peel'] = P_(
    f'Warm blush-cream background ({C}). Top 32%: the headline in huge heavy near-black ({D}) geometric sans, two centred lines: "TAPE CAME OFF" / "IN 10 MINUTES?". '
    'Middle 45%: on the left a small loose pile of three pale, washed-out, grey, desaturated strips of clear fashion tape, limp and curling at the edges, fading into the background; '
    'on the right ONE upright Savvy tube in full rich colour, sharply lit, casting a soft shadow, clearly the only strong element. '
    f'Bottom 13%: a rounded pink ({K}) pill with near-black bold text "Savvy holds up to 8 hours." That is ALL the text.', 'H')

P['T1_T_Bold'] = P_(
    f'Solid near-black ({D}) background. The headline fills about 60% of the canvas, flush left, stacked in three lines, heavy condensed sans-serif in warm cream ({C}), tight leading: '
    f'"TAPE CAME" / "OFF IN" / "10 MINUTES?" with only the words "10 MINUTES?" in pink ({K}). '
    f'Under it, small cream text "Savvy holds up to 8 hours." One small upright Savvy tube in the lower right corner, under 20% of the canvas height. That is ALL the text.', 'T')

P['T1_U_Cardboard'] = P_(
    'A flat piece of brown cardboard lying on a floor, photographed with harsh phone flash, slightly crooked. '
    'Big messy black marker handwriting fills the top two thirds: "TAPE CAME OFF IN 10 MINUTES?" across three lines. Below it in smaller marker: "Savvy holds up to 8 hours." '
    'One Savvy tube stands upright in front of the cardboard at the bottom right, sharp and legible. No other writing, no doodles.', 'U')

# ---------- T2: dance, don't adjust ----------
P['T2_F_Dance'] = P_(
    'Left 55%: a real Indian woman about 28, laughing mid-dance at a party, both arms raised high in the air, wearing a deep emerald satin noodle-strap top, framed from the waist up, '
    'warm blurred fairy lights behind, her eyes glancing to the right toward the text. '
    f'Right 45% on a clean warm blush-cream ({C}) panel: the headline in huge heavy near-black sans, two stacked lines: "DANCE." / "DON\'T ADJUST." '
    'Below it, small near-black text: "Savvy holds up to 8 hours." At the bottom of the panel one upright Savvy tube, large and legible. That is ALL the text.', 'F', real=True)

P['T2_A_Rooftop'] = P_(
    'Editorial photograph at golden hour on a rooftop terrace: two Indian friends, waist-up, laughing with their arms around each other, one in a satin noodle-strap top, '
    'one in a wide-neck cotton kurti, soft warm backlight, shallow depth of field, city lights blurred behind. '
    'In the sharp foreground at the bottom right, one upright Savvy tube standing on a stone ledge. '
    'Headline in the empty top-left sky area in large white heavy sans over a subtle darker gradient, two lines: "DANCE." / "DON\'T ADJUST." '
    'Small white text beneath: "Savvy holds up to 8 hours." That is ALL the text.', 'A', real=True)

P['T2_N_Flash'] = P_(
    'A casual phone photo taken with on-camera flash in a dim wedding hall: an Indian woman\'s hand holds one Savvy tube up toward the camera, large and sharp; '
    'background blurred colourful fairy lights and blurred dancing people. Slightly overexposed, grainy, off-centre. '
    'Near the top, text in a plain white default story-caption font on a thin translucent black bar: "DANCE. DON\'T ADJUST." '
    'A second smaller bar below it: "Savvy holds up to 8 hours." Nothing else.', 'N', real=True)

# ---------- T3: the trick is the wait ----------
P['T3_M_Minimal'] = P_(
    f'Warm off-white ({O}) background. Top 34%: the headline in huge heavy near-black grotesque, two centred lines: "THE TRICK" / "IS THE WAIT." '
    f'Centre: one upright Savvy tube, large, centred, soft studio shadow. Bottom: a rounded pink ({K}) pill with near-black text "Thin line. Wait 30 seconds. Press." That is ALL the text. Lots of empty space.', 'M')

P['T3_N_Notes'] = P_(
    f'A flat note page filling the whole canvas, cream paper colour ({C}) with faint horizontal lines, plain default sans-serif typography, no app chrome. '
    'A large bold black title line: "The trick is the wait." Then three short lines in regular weight, one under the other: "Thin line." / "Wait 30 seconds." / "Press." '
    'Below the text, a small rounded-corner photo inserted into the note, showing one upright Savvy tube on a plain white shelf. That is ALL the text.', 'N')

P['T3_U_Sticky'] = P_(
    'A flash photo of a yellow sticky note stuck slightly crooked on a bathroom mirror. Black marker handwriting on the note, big: "THE TRICK IS THE WAIT." and smaller below: "Thin line. Wait 30 seconds. Press." '
    'Under the note, on a small bathroom shelf, one upright Savvy tube, sharp and legible. Nothing else is written anywhere.', 'U')

# ---------- T4: even your maang tika ----------
P['T4_A_Flatlay'] = P_(
    'Top-down editorial flat-lay on a warm terracotta linen surface with soft window light. Exactly three objects, well spaced, lots of empty space: '
    'a gold maang tika with a small pearl drop (left), one Savvy tube lying flat (centre, hero, the largest object), and a neatly folded mustard block-print cotton kurti with its neckline showing (right). '
    f'Headline at the top in large heavy cream ({C}) sans, two lines: "EVEN YOUR" / "MAANG TIKA." Below it, small cream text: "Kurtis. Straps. Necklines." That is ALL the text.', 'A')

P['T4_F_Tika'] = P_(
    'Portrait of a real Indian woman about 30, three-quarter view, wearing a delicate gold maang tika centred on her hair parting and a soft mustard cotton kurti with a modest round neckline, '
    'natural window light, warm neutral background. She holds one upright Savvy tube near her shoulder, large and legible, and looks down at it with a small smile. '
    'Headline in the empty top-left space in large heavy near-black sans, two lines: "EVEN YOUR" / "MAANG TIKA." Small near-black text below it: "Kurtis. Straps. Necklines." That is ALL the text.', 'F', real=True)

P['T4_U_Notebook'] = P_(
    'A phone-flash photo of an open lined school notebook page on a desk, slightly crooked. Blue ballpoint-pen handwriting, large and messy but legible: "EVEN YOUR MAANG TIKA." on two lines, '
    'and smaller below it: "Kurtis. Straps. Necklines." One Savvy tube lying on the notebook page at the bottom right, sharp and legible. No drawings, no other words.', 'U')

# ---------- Bottom of funnel ----------
P['B1_P_Cards'] = P_(
    f'Warm off-white ({O}) background, strict centred grid. Top 32%: the headline in two centred lines of huge heavy near-black sans: "2 TUBES." / "RS 940." with the second line "RS 940." set inside a solid pink ({K}) rounded pill. '
    'Middle: two upright Savvy tubes side by side, equal size, equal spacing. Bottom: small near-black text "Besties Pack. Save Rs 420." That is ALL the text.', 'P')

P['B2_M_Three'] = P_(
    f'Solid soft pink ({K}) background. Top 32%: the headline in two centred lines of huge heavy near-black rounded sans: "3 TUBES." / "RS 1,350." with the second line set inside a solid cream ({C}) rounded pill. '
    'Middle: three upright Savvy tubes side by side in a tidy row, equal size, equal spacing. Bottom: small near-black text "Rs 450 a tube. Save Rs 690." That is ALL the text.', 'M')

P['B3_N_Order'] = P_(
    f'Blush-cream ({C}) background. Above the card, the headline in huge heavy near-black sans, two centred lines: "PAY WHEN" / "IT ARRIVES." '
    'Below it a clean white rounded order-summary card in plain default UI typography, three rows: row 1 a small photo thumbnail of one Savvy tube, the words "Savvy Body Glue" and on the right "Rs 680"; '
    'row 2 the word "Shipping" and on the right "Free"; row 3 the word "Payment" and on the right "Pay on delivery". No buttons, no other text.', 'N')


# ---------- Round 1b: UNAWARE top of funnel ----------
P['U1_N_Pins'] = P_(
    'A close phone-flash photo of an Indian woman\'s open palm holding a messy handful of about ten silver safety pins, slightly crooked, on a wooden dressing table, a folded silk blouse blurred behind. '
    'Near the top, text in a plain white default story-caption font on a thin translucent black bar: "SAFETY PINS HAD A GOOD RUN." '
    'One Savvy tube lying on the table at the bottom right, sharp and legible. A second smaller bar at the bottom left: "Meet Savvy Body Glue." Nothing else.', 'N', real=True)

P['U1_M_OnePin'] = P_(
    f'Solid soft pink ({K}) background. Top 32%: the headline in huge heavy near-black rounded sans, two centred lines: "SAFETY PINS" / "HAD A GOOD RUN." '
    'Middle: on the left one large silver safety pin lying at a slight angle with a soft shadow, on the right one upright Savvy tube in full colour, equal visual weight, plenty of space between them. '
    f'Bottom: a rounded cream ({C}) pill with near-black text "Meet Savvy Body Glue." That is ALL the text.', 'M')

P['U2_N_Circle'] = P_(
    'A casual phone-flash group photo at a wedding: four Indian women in festive sarees and lehengas posing with their arms around each other, smiling, slightly blurry, warm hall lights behind. '
    'The woman at the far right discreetly holds one hand at her neckline. A hand-drawn red marker circle is drawn around that hand. '
    'Bold white caption text with a thin black outline near the top: "THAT ONE HAND ON THE NECKLINE." Smaller white caption near the bottom: "There\'s a glue for that." '
    'In the bottom-right corner a small white-bordered sticker-style cut-out of one Savvy tube. Nothing else.', 'N', real=True)

P['U2_T_Hand'] = P_(
    f'Solid soft pink ({K}) background. The headline fills about 60% of the canvas, flush left, stacked in three lines, heavy condensed sans-serif in near-black ({D}), tight leading: "THAT ONE" / "HAND ON" / "THE NECKLINE." '
    'Under it, small near-black text: "There\'s a glue for that." One small upright Savvy tube in the lower right corner, under 20% of the canvas height. That is ALL the text.', 'T')

P['U3_A_Wardrobe'] = P_(
    'Editorial photograph inside an open wooden Indian wardrobe in warm light, silk sarees neatly folded on the shelves. In the centre one emerald-green silk blouse with a deep back neckline hangs on a wooden hanger, spotlit, with a small blank paper price tag still attached (no legible text on the tag). '
    'On the lower shelf edge at the bottom right, one upright Savvy tube. No people. '
    f'Headline in the darker upper-left area of the wardrobe interior in large heavy cream ({C}) sans, two lines: "THE BLOUSE" / "YOU NEVER WORE." Small cream text beneath: "Wear it. Savvy holds it in place." That is ALL the text.', 'A')

P['U3_N_Tag'] = P_(
    'A casual phone-flash photo in a slightly messy bedroom: an Indian woman\'s hand lifts a hanger holding a deep-neck mustard silk blouse with the price tag still attached (no legible text on the tag), an unmade bed behind. One Savvy tube lies on the bed at the bottom right, sharp and legible. '
    'Near the top, text in a plain white default story-caption font on a thin translucent black bar: "THE BLOUSE YOU NEVER WORE." A second smaller bar below it: "Wear it. Savvy holds it in place." Nothing else.', 'N', real=True)

P['U4_A_Demo'] = P_(
    'Top-down editorial photograph on a warm wooden table in soft window light: a mustard cotton kurti neckline lies flat, and an Indian hand (natural nails, one thin gold ring) squeezes a Savvy tube to draw a thin clear line of glue along the inside edge of the neckline. The tube is sharp, large and legible. No faces. '
    f'Headline in the empty space at the top in large heavy near-black sans, two lines: "YES, THERE\'S GLUE" / "FOR OUTFITS." Small near-black text beneath: "Thin line. Press. Done." That is ALL the text.', 'A', real=True)

P['U4_M_Glue'] = P_(
    f'Warm blush-cream ({C}) background. Top 34%: the headline in huge heavy deep forest-green (#1F4A34) rounded sans, two centred lines: "YES, THERE\'S GLUE" / "FOR OUTFITS." '
    f'Centre: one upright Savvy tube, large, centred, soft studio shadow. Bottom: a rounded pink ({K}) pill with near-black text "Thin line. Press. Done." That is ALL the text. Lots of empty space.', 'M')


if __name__ == '__main__':
    out = os.path.join(WORK, 'p'); os.makedirs(out, exist_ok=True)
    for k, v in P.items():
        open(os.path.join(out, k + '.txt'), 'w', encoding='utf-8').write(v)
    print(len(P), {k: len(v) for k, v in P.items()})
