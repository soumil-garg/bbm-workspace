PRE = "Generate an image. The attached photo is the exact product reference (MUFASA MAN OUD deodorant stick: matte black cylinder, silver lion crest, white MUFASA MAN wordmark, OUD label). Reproduce the product and its label faithfully wherever it appears. "
SUF = (" [NO PLATFORM CHROME] Render only the standalone ad creative, not a screenshot of how it displays in-feed. No device chrome, Sponsored labels, captions, engagement rows or buttons."
       " [EDGE-SAFE] All text and the product must fit within the central 84% of the canvas, about 8% padding from every edge. Backgrounds may bleed; text and focal elements may not touch or run off any edge."
       " [TEXT FIDELITY] Plain words only in body text, no emoji or special glyphs mid-sentence. Render exactly the text and number of items specified, do not invent extra words.")
REAL = (" PHOTOREALISM: shot on a full-frame camera, 35mm or 50mm lens, natural skin texture with pores, real fabric creases, true-to-life lighting, slight film grain. It must look like a real unretouched photograph of real people, not CGI, not illustration, not an AI render. Indian subjects, natural Indian skin tones. ")
P = {}

# ---- Batch 1: consumer voice (Amazon review language) ----
P['N1'] = PRE + ("1:1 static ad creative, 1080x1080, edge-to-edge. Template: comment thread, customer question and brand reply. Background: soft warm off-white #F4F1EC. "
 "Top half: a clean white rounded comment card in Instagram comment style (no app chrome), round grey avatar, username \"rohit.k_92\", comment text in regular black sans-serif: \"bro my deo is gone by lunch. I literally carry it to office now\". "
 "Below it, indented, a reply card with a small black round avatar showing the silver lion crest, username \"mufasaman\" with a small blue verified tick, reply text: \"Switch to a stick. One swipe at 8 AM, still smelling of oud at 8 PM.\" "
 "Exactly these two comments, nothing else. "
 "Bottom 40%: the MUFASA MAN OUD deodorant stick from the reference image standing upright on a dark stone surface with a few pieces of oud wood, soft warm studio light, premium product photography. Small text under it: \"Oud Deo Stick | mufasaman.com\"." + SUF)
P['N2'] = PRE + ("1:1 static ad creative, 1080x1080, edge-to-edge. Template: bold typography hero statement. Canvas: deep matte black #111111. "
 "Left two-thirds: a huge chunky condensed sans-serif statement in off-white #F4F1EC, three stacked lines, very large, tight leading, ending with a period: \"GONE BY\" / \"LUNCH?\" / \"NOT THIS.\" The word \"NOT THIS.\" is in warm amber #D4A25A. "
 "Lower-left, smaller regular sans-serif in light grey, four short lines: \"Most deos fade in 2 hours.\" / \"This oud stick lasts the day.\" / \"No gas. No alcohol.\" / \"No white marks.\" "
 "Right third: the MUFASA MAN OUD deodorant stick from the reference image standing upright, cap off beside it showing the white balm, dramatic rim light, a thin wisp of warm smoke rising behind it. Brutalist, confident, premium." + SUF)
P['N3'] = PRE + ("1:1 static ad creative, 1080x1080. Template: handwritten testimonial on paper. Photoreal top-down photo of a dark walnut desk. On it, a torn sheet of cream notebook paper with a handwritten note in blue ballpoint pen, natural imperfect handwriting, exactly these words: \"The fragrance is very premium, bold and classy. A proper rich oud smell. And it's a deodorant!\" "
 "Below the handwriting, five small hand-drawn stars. Beside the paper: the MUFASA MAN OUD deodorant stick from the reference image lying at a slight angle, a steel wristwatch and a pair of sunglasses. Warm window light from the left, soft shadows. "
 "Top of the image, clean bold off-white sans-serif headline on a subtle dark gradient band: \"WHAT BUYERS ARE SAYING\". Bottom right small text: \"Verified buyer review\"." + SUF)

# ---- Batch 2: competitor-inspired ----
P['N4'] = PRE + ("1:1 static ad creative, 1080x1080. Inspired by the annotated product-on-clothes format used by leading refillable deodorant brands. "
 "Photoreal top-down photo: a neatly folded crisp black cotton shirt on a light linen surface, the MUFASA MAN OUD deodorant stick from the reference image lying diagonally on the shirt, cap off showing the white balm. Soft daylight. "
 "Three small rounded white callout bubbles with thin hand-drawn arrows pointing to the shirt and product, each with a small amber check mark and short black sans-serif text: \"No white marks\", \"0% alcohol\", \"Oud that lasts all day\". "
 "Top, centred, bold black sans-serif headline: \"SAFE FOR BLACK SHIRTS.\" Bottom centred small text: \"Mufasa Man Oud Deo Stick\". Clean, bright, trustworthy." + SUF)
P['N5'] = PRE + ("1:1 static ad creative, 1080x1080. Inspired by value-counting mass-market deo ads. Template: big stat hero. Background warm off-white #F4F1EC. "
 "Top-left: a giant bold black condensed number \"\u20b96\" with small text beside it \"a day\". Under it, bold black sans-serif line: \"Less than your cutting chai.\" "
 "Middle-right: a photoreal glass of cutting chai on a small steel saucer next to the MUFASA MAN OUD deodorant stick from the reference image, both on a wooden counter, warm morning light. "
 "Bottom band, dark #111111 strip with off-white text: \"One stick lasts up to 6 months  |  \u20b91,053\". Clean, witty, premium." + SUF)
P['N6'] = PRE + ("1:1 static ad creative, 1080x1080. Inspired by luxury fragrance-brand still-life ads. Template: editorial ingredient still life. "
 "Dark moody scene: the MUFASA MAN OUD deodorant stick from the reference image stands on a slab of dark stone, surrounded by raw oud wood chips, a few amber resin crystals and a strip of cognac leather, a slow curl of smoke rising from a smouldering oud chip behind it. Low-key chiaroscuro lighting, warm amber highlights, deep shadows. "
 "Top centred, elegant large serif headline in off-white: \"IT'S A DEO.\" and on the next line in amber italic serif: \"It smells like oud.\" "
 "Bottom centred, small spaced-out sans caps in grey: \"SMOKY OUD  \u00b7  AMBER  \u00b7  LEATHER\". Luxurious, minimal." + SUF)

# ---- Batch 3: real people, photoreal, scroll-stopping ----
P['N7'] = PRE + REAL + ("1:1 static ad creative, 1080x1080. Photograph inside a crowded Mumbai local train at evening rush hour. A confident Indian man, late 20s, in a fitted crisp black shirt, stands with his arm raised holding the overhead grab handle, relaxed half-smile, looking slightly off-camera. His raised underarm is clean and dry, no sweat patches, no white marks. People around him slightly out of focus, warm tungsten light and window glare, real candid documentary feel. "
 "Top-left, bold off-white condensed sans-serif headline with a subtle shadow for legibility: \"ARMS UP.\" / \"ZERO PANIC.\" "
 "Bottom-right corner: a small clean inset of the MUFASA MAN OUD deodorant stick from the reference image with small off-white text \"Oud Deo Stick\"." + SUF)
P['N8'] = PRE + REAL + ("1:1 static ad creative, 1080x1080. Photograph in a real Indian apartment bathroom in the morning, soft window light. Close mid-shot of an Indian man, early 30s, towel on shoulder, applying the MUFASA MAN OUD deodorant stick from the reference image to his underarm, the product label clearly visible and faithful, candid natural moment, a little steam on the mirror edge. "
 "Top of image, bold off-white sans-serif headline on a subtle dark gradient: \"1 SWIPE AT 8 AM.\" and on the next line in amber #D4A25A: \"STILL OUD AT 8 PM.\"" + SUF)
P['N9'] = PRE + REAL + ("1:1 static ad creative, 1080x1080. Photograph at a warm candle-lit rooftop restaurant at night. An Indian woman, late 20s, leans in close towards an Indian man's neck and shoulder while laughing, eyes closed, as if she just noticed how good he smells; he wears a black shirt and smiles. Shallow depth of field, warm bokeh lights, intimate candid moment, real skin and fabric texture. "
 "Top-left, elegant large off-white serif headline: \"She leaned in.\" Under it, smaller sans-serif in amber #D4A25A: \"That's the oud.\" "
 "Bottom-right corner: small clean inset of the MUFASA MAN OUD deodorant stick from the reference image." + SUF)

for k, v in P.items():
    open(f'C:/cca/mufasa/p/{k}.txt', 'w', encoding='utf-8').write(v)
print({k: len(v) for k, v in P.items()})
