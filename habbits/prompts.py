PRE = ("Generate an image. The attached photo is the exact product reference sheet for the Indian oral-care brand HABBITS. It shows 8 products: "
       "Te-Cha Charcoal Mint Toothpaste (matte black tube, vertical white 'Habbits' serif wordmark), Apple Mint Toothpaste (white tube, black wordmark), "
       "Natural Whitening Powder (matte black jar with a white tooth logo), Advance Whitening Serum (slim black pump bottle and black box), "
       "Charcoal Whitening Mouthwash (black bottle, white tooth logo), Sensitivity Relief Mouthwash (clear bottle, green tooth logo), Copper Tongue Cleaner, Wheat-straw toothbrushes. "
       "Reproduce every product you show and its label faithfully: matte black and white packaging, the 'Habbits' wordmark, the tooth logo. Do not invent other products or brands. ")
SUF = (" [NO PLATFORM CHROME] Render only the standalone ad creative, not a screenshot of how it displays in-feed. No device chrome, Sponsored labels, captions, engagement rows or buttons."
       " [EDGE-SAFE] All text and products must fit within the central 84% of the canvas, about 8% padding from every edge. Backgrounds may bleed; text and focal elements may not touch or run off any edge."
       " [TEXT FIDELITY] Plain words only in body text, no emoji or special glyphs mid-sentence. Render exactly the text and number of items specified, do not invent extra words, prices or claims.")
REAL = (" PHOTOREALISM: shot on a full-frame camera, 35mm or 50mm lens, natural skin texture with pores, real fabric creases, true-to-life lighting, slight film grain. "
        "It must look like a real unretouched photograph of real people, not CGI, not illustration, not an AI render. Indian subjects, natural Indian skin tones. ")
OFFER_BADGE = ("a bold rounded badge in lime #C9F24B with black heavy sans-serif text \"BUY 2 GET 1 FREE\"")
P = {}

# ---- Batch A: consumer voice ----
P['A1_OneTube'] = PRE + ("1:1 static ad creative, 1080x1080. Template: bold typography hero statement (brutalist). Canvas: matte black #111111. "
 "Top 55%: huge chunky condensed sans-serif headline in off-white #F4F1EC, three stacked lines, very tight leading: \"ONE TUBE\" / \"WON'T DO IT.\" / \"THREE WILL.\" The words \"THREE WILL.\" are in lime #C9F24B. "
 "Below it, one line of regular sans-serif in light grey: \"Stains need a routine, not a single product.\" "
 "Bottom 40%: three HABBITS products standing side by side on a dark stone ledge with soft rim light: the black Te-Cha Charcoal Mint Toothpaste, the black Natural Whitening Powder jar, and the slim black Advance Whitening Serum pump bottle. "
 "Above the third product (the serum) a small lime tag with black text \"FREE\". Bottom-right corner: " + OFFER_BADGE + ". Premium, confident, monochrome with one lime accent." + SUF)

P['A2_Comment'] = PRE + ("1:1 static ad creative, 1080x1080. Template: fake comment thread, customer question and brand reply. Background: soft warm off-white #F4F1EC. "
 "Top 55%: a clean white rounded comment card (no app chrome), round grey avatar, username \"priya.s_blr\", comment text in regular black sans-serif: \"tried a whitening toothpaste for a month, still yellow. what actually works??\" "
 "Below it, indented, a reply card with a small black round avatar showing a white tooth logo, username \"habbits.in\" with a small blue verified tick, reply text: \"Paste alone is step one. Add the powder and the serum. And right now the third one is free.\" "
 "Exactly these two comments, nothing else. "
 "Bottom 40%: the black Te-Cha Charcoal Mint Toothpaste, the black Natural Whitening Powder jar and the black Advance Whitening Serum lined up on a white marble bathroom counter with soft window light, premium product photography. "
 "Small bold black text under them: \"Pick any 3. Pay for 2.\"" + SUF)

P['A3_Checklist'] = PRE + ("1:1 static ad creative, 1080x1080. Template: pain-point checklist with product. Canvas: off-white #F4F1EC. "
 "Top: bold black condensed sans-serif headline: \"3 PROBLEMS. PAY FOR 2.\" "
 "Left half: a vertical checklist of three rows, each row a black rounded square with a lime #C9F24B check mark and bold black sans-serif text: \"Chai and coffee stains\", \"Morning breath\", \"Sensitive teeth\". "
 "Next to each row, on the right half, the matching HABBITS product photographed cleanly: row 1 the black Natural Whitening Powder jar, row 2 the black Charcoal Whitening Mouthwash bottle, row 3 the clear Sensitivity Relief Mouthwash bottle with the green tooth logo. "
 "Bottom band: matte black #111111 strip with off-white text \"Add any 3 to cart. The 3rd one is on us.\" and on the right " + OFFER_BADGE + ". Clean, organised, trustworthy." + SUF)

# ---- Batch B: Hismile / competitor-inspired ----
P['B1_WhoGetsFree'] = PRE + ("1:1 static ad creative, 1080x1080. Inspired by gifting-style bundle ads. Background: bold lime #C9F24B. "
 "Top: huge heavy black sans-serif headline, slightly tilted, two lines: \"WHO GETS\" / \"YOUR FREE ONE?\" "
 "Middle: three HABBITS products standing in a row, large and crisp: the black Te-Cha Charcoal Mint Toothpaste, the white Apple Mint Toothpaste, and the black Charcoal Whitening Mouthwash. "
 "Each has a handwritten-style white paper tag hanging from it with black marker text: first tag \"ME\", second tag \"ME\", third tag \"MUMMY\". "
 "Bottom: a black rounded pill with lime text \"BUY 2 GET 1 FREE\" and under it small black text \"Pick any 3 at habbits.in\". Playful, loud, scroll-stopping." + SUF)

P['B2_Margins'] = PRE + ("1:1 static ad creative, 1080x1080. Inspired by 'we messed up our margins' offer ads. Background: deep matte black #111111 with a subtle warm spotlight from the top. "
 "Top-left: a small lime warning triangle icon, then a bold off-white sans-serif headline, two lines: \"Our accountant\" / \"is not happy.\" "
 "Under it, regular grey sans-serif, two short lines: \"Add any 3 Habbits products.\" / \"Pay for only 2. Seriously.\" "
 "Bottom 55%: two groups of products on a dark stone surface. Left group labelled with a small white rounded tag \"buy 2\": the black Natural Whitening Powder jar and the black Advance Whitening Serum. A large lime plus sign between the groups. "
 "Right group labelled with a lime rounded tag \"1 free\": the black Charcoal Whitening Mouthwash bottle. Clean studio lighting, premium, witty." + SUF)

P['B3_Receipt'] = PRE + ("1:1 static ad creative, 1080x1080. Template: cash register receipt. Photoreal top-down photo of a crumpled-then-flattened white thermal paper receipt on a matte black surface, beside it the black Te-Cha Charcoal Mint Toothpaste, the black Natural Whitening Powder jar and the black Advance Whitening Serum lying at slight angles. Soft daylight. "
 "The receipt has monospaced black thermal text, exactly these lines: header \"HABBITS\", then \"TE-CHA TOOTHPASTE   249.00\", \"WHITENING POWDER    448.00\", \"WHITENING SERUM     549.00\", a dashed line, \"BUY 2 GET 1 FREE   -249.00\", then bold \"YOU PAY            997.00\". "
 "The line \"BUY 2 GET 1 FREE\" is circled by hand in a lime #C9F24B marker. "
 "Top of the image, bold off-white condensed sans-serif headline on the black surface: \"BEST RECEIPT YOU'LL SEE TODAY.\" Keep every receipt line crisp and legible, no extra lines." + SUF)

# ---- Batch C: real people, Indian settings ----
P['C1_Ordered2'] = PRE + REAL + ("1:1 static ad creative, 1080x1080. Photograph at the front door of a modern Indian apartment in the evening. A young Indian woman, mid 20s, in a casual oversized t-shirt, has just opened a black HABBITS delivery box, holding up three products with a delighted surprised laugh: the black Te-Cha Charcoal Mint Toothpaste, the black Natural Whitening Powder jar and the black Advance Whitening Serum. Warm hallway light, candid documentary feel. "
 "Top-left, bold off-white condensed sans-serif headline with a subtle shadow for legibility: \"PAID FOR 2.\" / \"GOT 3.\" with \"GOT 3.\" in lime #C9F24B. "
 "Bottom-right: " + OFFER_BADGE + "." + SUF)

P['C2_Flatmates'] = PRE + REAL + ("1:1 static ad creative, 1080x1080. Photograph in a real shared Indian flat bathroom in the morning, soft window light. Two Indian flatmates in their mid 20s, a young man and a young woman, stand at the sink brushing their teeth, laughing at each other in the mirror, casual and candid. "
 "On the counter in front of them, clearly visible and faithful: the black Te-Cha Charcoal Mint Toothpaste, the white Apple Mint Toothpaste and the black Charcoal Whitening Mouthwash. "
 "Top of image, bold off-white sans-serif headline on a subtle dark gradient, three short words on one line: \"MINE. YOURS. FREE.\" with \"FREE.\" in lime #C9F24B. "
 "Bottom-left small off-white text: \"Buy any 2, get 1 free | habbits.in\"." + SUF)

P['C3_Shaadi'] = PRE + REAL + ("1:1 static ad creative, 1080x1080. Photograph of an Indian wedding-season getting-ready moment: a young Indian woman in a rich silk saree and gold jewellery, hair half done, sits at a vanity with warm bulb lights, smiling a wide bright confident smile at her reflection. "
 "On the vanity, clearly visible and faithful: the slim black Advance Whitening Serum, the black Natural Whitening Powder jar and the black Charcoal Whitening Mouthwash, among bangles and a makeup brush. Warm golden light, candid, festive. "
 "Top-left, elegant large off-white serif headline: \"Shaadi season smile.\" Under it, smaller bold sans-serif in lime #C9F24B: \"3 steps. Pay for 2.\"" + SUF)

import os
os.makedirs('C:/cca/habbits/p', exist_ok=True)
for k, v in P.items():
    open(f'C:/cca/habbits/p/{k}.txt', 'w', encoding='utf-8').write(v)
print({k: len(v) for k, v in P.items()})
