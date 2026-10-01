PRE = ("Generate an image. The attached photo is the exact product reference sheet for the Indian oral-care brand HABBITS. It shows 8 products: "
       "Te-Cha Charcoal Mint Toothpaste (matte black tube, vertical white 'Habbits' serif wordmark), Apple Mint Toothpaste (white tube, black wordmark), "
       "Natural Whitening Powder (matte black jar with a white tooth logo), Advance Whitening Serum (slim black pump bottle), "
       "Charcoal Whitening Mouthwash (black bottle, white tooth logo), Sensitivity Relief Mouthwash (clear bottle, green tooth logo), Copper Tongue Cleaner, Wheat-straw toothbrushes. "
       "Reproduce every product you show exactly as in the reference: same shape, matte black or white packaging, the 'Habbits' wordmark, the tooth logo, same label layout. Do not add taglines or text to labels that are not in the reference. Do not invent other products or brands. ")

DESIGN = (" [DESIGN RULES - follow strictly] Minimal, premium, uncluttered poster. ONE focal point: the headline is the single most dominant element, at least 3 times larger than any other text. "
          "Render ONLY the text listed in this prompt, nothing else anywhere. At least 40% of the canvas is empty negative space with generous, even spacing between the headline, the products and the offer. "
          "No decorative props of any kind: no leaves, flowers, fruit, charcoal pieces, stones, powder splashes, icons, stickers, arrows, badges or borders unless explicitly described. "
          "Colour rule 60-30-10: background colour fills about 60%, products about 30%, the lime accent #C9F24B about 10% and is used on ONE element only. "
          "All elements aligned on a single centre axis. Clean soft studio light, crisp product photography, high contrast, bold modern grotesque sans-serif type.")

SUF = (" [NO PLATFORM CHROME] Render only the standalone ad creative. No device chrome, Sponsored labels, captions, engagement rows or buttons."
       " [EDGE-SAFE] All text and products stay within the central 84% of the canvas, about 8% padding from every edge; nothing touches or runs off an edge."
       " [TEXT FIDELITY] Render exactly the words specified, spelled exactly, no extra words, prices or claims.")

REAL = (" PHOTOREALISM: full-frame camera, 50mm lens, natural skin texture, true-to-life lighting, slight film grain. Looks like a real unretouched photograph, not CGI or illustration. "
        "Indian subject, natural Indian skin tone. Anatomy must be correct: exactly two arms and two hands, five fingers on each hand, no extra limbs. ")

TRIO = "three products standing upright side by side with equal spacing: the black Te-Cha Charcoal Mint Toothpaste, the black Natural Whitening Powder jar and the slim black Advance Whitening Serum"
P = {}

P['R1_Buy2Get1'] = PRE + ("1:1 static ad creative, 1080x1080. Background: solid matte black #111111. "
 "Top 35%: the headline in huge heavy off-white #F4F1EC condensed sans-serif, two centred lines: \"BUY 2.\" / \"GET 1 FREE.\" with \"GET 1 FREE.\" in lime #C9F24B. "
 "Middle 45%: " + TRIO + ", on a subtle dark floor with a soft reflection. "
 "Bottom: small off-white text centred: \"habbits.in\". That is ALL the text: 5 words in total." + DESIGN + SUF)

P['R2_OneTube'] = PRE + ("1:1 static ad creative, 1080x1080. Background: solid matte black #111111. "
 "Top 40%: the headline in huge heavy off-white #F4F1EC condensed sans-serif, two centred lines: \"ONE TUBE\" / \"WON'T DO IT.\" "
 "Middle 40%: " + TRIO + ". "
 "Below the products, one small centred line in lime #C9F24B: \"The 3rd one is free.\" That is ALL the text: 9 words in total." + DESIGN + SUF)

P['R3_WhoGetsFree'] = PRE + ("1:1 static ad creative, 1080x1080. Background: solid lime #C9F24B (here lime is the 60% background, and black is the accent). "
 "Top 30%: the headline in huge heavy black #111111 sans-serif, two centred lines: \"WHO GETS\" / \"YOUR FREE ONE?\" "
 "Middle 50%: three products side by side with equal spacing: the black Te-Cha Charcoal Mint Toothpaste, the white Apple Mint Toothpaste and the black Charcoal Whitening Mouthwash. "
 "Each has one small plain white paper tag on a thin string with black handwritten marker text: first \"ME\", second \"ME\", third \"MUMMY\". "
 "Bottom: one small black rounded pill with lime text \"BUY 2 GET 1 FREE\". That is ALL the text." + DESIGN + SUF)

P['R4_Accountant'] = PRE + ("1:1 static ad creative, 1080x1080. Background: solid warm off-white #F4F1EC. "
 "Top 35%: the headline in huge heavy black #111111 sans-serif, two centred lines: \"OUR ACCOUNTANT\" / \"IS NOT HAPPY.\" "
 "Middle 45%: " + TRIO + ". The serum on the right has one small lime #C9F24B rounded tag above it with black text \"FREE\". "
 "Bottom: one small centred black line: \"Buy any 2, get 1 free.\" That is ALL the text." + DESIGN + SUF)

P['R5_3Problems'] = PRE + ("1:1 static ad creative, 1080x1080. Background: solid warm off-white #F4F1EC. "
 "Top 30%: the headline in huge heavy black #111111 sans-serif, one or two centred lines: \"3 PROBLEMS.\" / \"PAY FOR 2.\" with \"PAY FOR 2.\" in black on a lime #C9F24B highlight bar. "
 "Middle 50%: three products standing in a row with wide equal spacing: the black Natural Whitening Powder jar, the black Charcoal Whitening Mouthwash, the clear Sensitivity Relief Mouthwash with the green tooth logo. "
 "Directly under each product one small grey word: \"Stains\", \"Breath\", \"Sensitivity\". That is ALL the text: 8 words in total." + DESIGN + SUF)

P['R6_PickAny3'] = PRE + ("1:1 static ad creative, 1080x1080. Clean top-down flatlay on a plain warm off-white #F4F1EC surface. "
 "Top 30%: the headline in huge heavy black #111111 sans-serif, two centred lines: \"PICK ANY 3.\" / \"PAY FOR 2.\" "
 "Lower 55%: three products lying flat, spaced far apart in a neat row with lots of empty surface around them: the white Apple Mint Toothpaste, the black Charcoal Whitening Mouthwash and the Copper Tongue Cleaner. "
 "The third product (the copper tongue cleaner) sits on a small lime #C9F24B circle. That is ALL the text: 6 words." + DESIGN + SUF)

P['R7_3rdOnUs'] = PRE + ("1:1 static ad creative, 1080x1080. Background: solid matte black #111111. "
 "Top 35%: the headline in huge heavy off-white #F4F1EC sans-serif, two centred lines: \"THE 3RD ONE\" / \"IS ON US.\" "
 "Middle 45%: " + TRIO + ". Only the serum on the right has a thin lime #C9F24B satin ribbon tied around it with a small neat bow, like a gift. "
 "Bottom: one small centred off-white line: \"Buy 2, get 1 free.\" That is ALL the text." + DESIGN + SUF)

P['R8_StockUp'] = PRE + REAL + ("1:1 static ad creative, 1080x1080. Photograph against a plain smooth warm off-white #F4F1EC wall, nothing else in the background. "
 "An Indian woman in her mid 20s in a plain black t-shirt, framed from the chest up in the lower 60% of the image, smiling a wide natural bright smile at camera, holding up three products fanned out in her two hands at chest height, labels facing camera: the black Te-Cha Charcoal Mint Toothpaste, the black Natural Whitening Powder jar and the slim black Advance Whitening Serum. "
 "Top 30%: the headline in huge heavy black #111111 sans-serif, centred: \"BUY 2. GET 1 FREE.\" with \"GET 1 FREE.\" on a lime #C9F24B highlight bar. That is ALL the text." + DESIGN + SUF)

P['R9_TwoPlusOne'] = PRE + ("1:1 static ad creative, 1080x1080. Background: solid matte black #111111. "
 "Top 50%: a giant typographic equation in heavy off-white #F4F1EC sans-serif, centred, filling most of the width: \"2 + 1\". Directly under the \"1\", one lime #C9F24B word in bold caps: \"FREE\". "
 "Lower 35%: " + TRIO + ", smaller, neat. "
 "Bottom: one small centred off-white line: \"Any 3 Habbits products.\" That is ALL the text." + DESIGN + SUF)

import os
os.makedirs('C:/cca/habbits/p2', exist_ok=True)
for k, v in P.items():
    open(f'C:/cca/habbits/p2/{k}.txt', 'w', encoding='utf-8').write(v)
print({k: len(v) for k, v in P.items()})
