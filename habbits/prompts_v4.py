PRE = ("Generate an image. The attached photo is the exact product reference sheet for the Indian oral-care brand HABBITS. It shows 8 products, left to right, top row: "
       "Te-Cha Charcoal Mint Toothpaste (matte black tube, vertical white 'Habbits' wordmark), Apple Mint Toothpaste (white tube, black wordmark), Natural Whitening Powder (matte black jar, tooth logo), Advance Whitening Serum (slim black pump bottle); "
       "bottom row: Charcoal Mouthwash (black bottle, white label with black tooth), Sensitivity Mouthwash (clear bottle, green tooth), Copper Tongue Cleaner (copper loop, cream box), Wheat-straw Toothbrushes (beige handles, black bristles). "
       "Reproduce every product you show exactly as in the reference: same shape, colours, 'Habbits' wordmark, tooth logo and label layout. Show ONLY the product containers: no grapefruit, flowers, mint leaves, charcoal pieces, paste smears, stones, plates, vanilla or other props from the reference, and no 'Indian Angels' badge. "
       "Do not add text to labels. Do not invent products or brands. ")
SUF = (" [NO PLATFORM CHROME] Standalone ad creative only. No phone status bar, device frame, Sponsored label, captions, like counts or app buttons unless explicitly described."
       " [EDGE-SAFE] All text and products within the central 84% of the canvas, about 8% padding from every edge."
       " [TEXT FIDELITY] Render exactly the words in double quotes, spelled exactly, with exactly these prices; no extra words, numbers or claims anywhere.")
REAL = (" PHOTOREALISM: full-frame camera, 50mm, natural skin texture, true-to-life light, slight grain; a real unretouched photograph, not CGI. Indian subject, natural Indian skin tone. Correct anatomy: one hand has exactly five fingers. ")
SYS = {
'M': " [DESIGN SYSTEM: MINIMAL SWISS] Premium, uncluttered. The headline is the dominant element, at least 3x larger than any other text. At least 35% empty space. Warm off-white #F4F1EC background, lime #C9F24B used on one element only. Single centre axis. Soft even studio light, heavy modern grotesque sans-serif.",
'T': " [DESIGN SYSTEM: BOLD TYPOGRAPHY] Type is the hero, filling about 60% of the canvas, heavy condensed sans-serif, tight leading, flush left. Products small. Two colours plus lime. No decorations.",
'P': " [DESIGN SYSTEM: PROOF AND DATA] Clean information design where the prices are the hero. Strict grid, precise alignment, tabular figures, generous spacing, black on warm off-white #F4F1EC, lime #C9F24B only on the pay-price.",
'N': " [DESIGN SYSTEM: NATIVE] Looks like a real, plain e-commerce cart screen someone screenshotted, not a designed ad: default UI font, white card, thin grey dividers, no brand styling beyond the product photos.",
'F': " [DESIGN SYSTEM: HAND AND GAZE] A real hand is the entry point and its motion leads the eye to the chosen product and the offer. Product large and legible. Headline in clean empty space.",
'U': " [DESIGN SYSTEM: DELIBERATELY UGLY] Unpolished, homemade, real-shop feel: flat phone flash, slightly crooked framing, thick marker handwriting on brown cardboard. The sign text must still be large and perfectly legible.",
}


def P_(body, s, real=False):
    return PRE + (REAL if real else "") + "1:1 static ad creative, 1080x1080. " + body + SYS[s] + SUF


P = {}
P['B1_M_PickAny3'] = P_("Top 32%: headline in huge heavy black #111111 sans-serif, two centred lines: \"PICK ANY 3.\" / \"PAY FOR 2.\" with \"PAY FOR 2.\" sitting on a lime #C9F24B highlight bar. Directly below, one small grey line: \"Mix any Habbits products. The cheapest one is free.\" Lower 50%: all 8 products standing in two neat, evenly spaced rows of four on the plain background. That is ALL the text.", 'M')
P['B2_P_Combos'] = P_("Top 20%: headline in heavy black sans-serif, centred: \"ANY 3. PAY FOR 2.\" Below it, three equal white cards side by side, each with its three small products on top and text underneath. Card 1: title \"WHITENING\", products Te-Cha toothpaste, Whitening Powder, Whitening Serum, a struck-through grey \"₹1,246\" and a large bold \"₹997\" on a lime highlight. Card 2: title \"FRESH BREATH\", products Te-Cha toothpaste, Charcoal Mouthwash, Copper Tongue Cleaner, struck-through \"₹896\" and large bold \"₹647\" on lime. Card 3: title \"GENTLE\", products Apple Mint toothpaste, Sensitivity Mouthwash, Copper Tongue Cleaner, struck-through \"₹896\" and large bold \"₹647\" on lime. Bottom: one small centred grey line: \"Or build your own.\" That is ALL the text.", 'P')
P['B3_T_Any3'] = P_("Background solid matte black #111111. Headline flush left filling the upper 65%, huge heavy condensed sans-serif, three lines: \"ANY\" / \"3.\" in off-white #F4F1EC and \"PAY FOR 2.\" in lime #C9F24B. Below it one small off-white line: \"Mix any Habbits products.\" Bottom 18%: all 8 products small in one neat row. That is ALL the text.", 'T')
P['B4_N_Cart'] = P_("Warm off-white #F4F1EC background. Top 20%: headline in heavy black sans-serif, centred, two lines: \"ADD ANY 3.\" / \"ONE GOES ₹0.\" Centre: a clean white e-commerce cart card with soft shadow, header \"Your cart\", and exactly three line items, each with a small product photo on the left, name in the middle, price on the right: \"Whitening Serum\" \"₹549\"; \"Whitening Powder\" \"₹448\"; \"Te-Cha Toothpaste\" with its price shown as a grey struck-through \"₹249\" next to a green \"FREE\". A thin divider, then a bold final row: \"You pay\" \"₹997\". That is ALL the text.", 'N')
P['B5_F_Pick'] = P_("A clean, minimal off-white shelf holding all 8 products in a neat row, softly lit. A real Indian woman's hand with a thin gold ring enters from the right, fingers wrapped around the Whitening Serum, lifting it off the shelf; two other products (Te-Cha toothpaste and Whitening Powder) are already pulled slightly forward on the shelf. Top 30% plain wall: headline in huge heavy black sans-serif, centred, two lines: \"PICK ANY 3.\" / \"PAY FOR 2.\" and one small grey line: \"The cheapest one is free.\" That is ALL the text.", 'F', real=True)
P['B6_U_Kirana'] = P_("Flash photo on a small Indian shop counter. A piece of torn brown cardboard is propped up in the centre with thick black marker handwriting in big capitals, three lines: \"KOI BHI 3 LO.\" / \"2 KA PAISA DO.\" and below, smaller, underlined: \"Habbits\". In front of the sign on the counter, a messy but clear group of Habbits products: Te-Cha toothpaste, Apple Mint toothpaste, Whitening Powder, Whitening Serum, Charcoal Mouthwash. Slightly crooked framing. That is ALL the text.", 'U')

import os
os.makedirs('C:/cca/habbits/p4', exist_ok=True)
for k, v in P.items():
    open(f'C:/cca/habbits/p4/{k}.txt', 'w', encoding='utf-8').write(v)
print(len(P), {k: len(v) for k, v in P.items()})
