PRE = ("Generate an image. The attached photo is the exact product reference (ASHOPI Brass Ashtalakshmi Kalash: a round-bellied polished yellow-gold brass pot with a wide flared mouth, dense hand-engraved floral and paisley patterns, a band of raised figures of Goddess Lakshmi seated in arched niches around the belly, antique golden finish, about 5.5 inches tall). "
       "Reproduce the product faithfully wherever it appears, same shape, same engraving, same Lakshmi figures, same finish. Do not add a logo or text onto the kalash. ")
SUF = (" [NO PLATFORM CHROME] Render only the standalone ad creative, not a screenshot of how it displays in-feed. No device chrome, Sponsored labels, captions, engagement rows or buttons."
       " [EDGE-SAFE] All text and the product must fit within the central 84% of the canvas, about 8% padding from every edge. Backgrounds may bleed; text and focal elements may not touch or run off any edge."
       " [TEXT FIDELITY] Plain words only in body text, no emoji or special glyphs mid-sentence. Render exactly the text and number of items specified, do not invent extra words.")
REAL = (" PHOTOREALISM: shot on a full-frame camera, 50mm lens, natural skin texture with pores, real fabric creases and saree drape, true-to-life warm lighting, slight film grain. It must look like a real unretouched photograph of real people, not CGI, not illustration, not an AI render. Indian subject, natural Indian skin tone. ")
P = {}

# 1. Consumer voice: buyers complain kalash arrive 'too small to use in pooja'. Annotated callouts.
P['KAL1'] = PRE + ("1:1 static ad creative, 1080x1080. Template: annotated product callouts. Background: warm ivory #F6EFE3 with a very soft paper texture. "
 "Top 22%: bold deep maroon #6B1E1E condensed serif-sans headline, two lines, very large: \"NOT A TINY\" / \"SHOWPIECE.\" "
 "Centre 60%: the brass Ashtalakshmi kalash from the reference, large and upright on a plain white marble surface, soft natural window light from the left, crisp realistic shadow, premium product photography. "
 "Four thin dark hand-drawn arrows point from the kalash to four short labels in bold dark charcoal #222222 sans-serif, two on each side: \"5.5 inch tall\", \"6 inch wide\", \"450 g pure brass\", \"8 Lakshmi forms, hand-engraved\". "
 "Bottom 12%: a thin maroon line, and under it small charcoal sans-serif text: \"Big enough for your mandir. Made by Aakrati since 1998.\"" + SUF)

# 2. Consumer voice: pain checklist (size, fake metal, damage in transit).
P['KAL2'] = PRE + ("1:1 static ad creative, 1080x1080. Template: pain checklist. Left 55% of the canvas is a solid deep maroon #5A1414 panel; right 45% shows the brass Ashtalakshmi kalash from the reference on a dark carved wooden pooja chowki, warm diya light glowing beside it, a few marigold flowers, rich cinematic product photography. "
 "On the maroon panel, top: bold cream #F6EFE3 sans-serif headline, three lines: \"BEFORE YOU BUY\" / \"A KALASH,\" / \"CHECK THIS.\" "
 "Below it, exactly four checklist rows, each with a gold #D4A441 tick mark and cream sans-serif text: \"Real size, 5.5 inch tall\", \"100% pure brass\", \"Handcrafted by Aakrati, since 1998\", \"Packed safe in a branded box\". "
 "Bottom of the maroon panel, small gold sans-serif text: \"ashopi.com\". Exactly four rows, no more." + SUF)

# 3. Category playbook: Dhanteras metal-buying + price anchor. Bold typography.
P['KAL3'] = PRE + ("1:1 static ad creative, 1080x1080. Template: bold typography hero with price. Background: deep festive maroon #4A0E0E with a very subtle gold mandala pattern at 8% opacity. "
 "Top 30%: huge bold cream #F6EFE3 condensed sans-serif headline in Hinglish, two lines: \"IS DHANTERAS,\" / \"BRASS GHAR LAO.\" "
 "Centre: the brass Ashtalakshmi kalash from the reference glowing under warm light, standing on a small bed of marigold petals, a few lit clay diyas around it, soft bokeh. "
 "Bottom 22%: left side, a large bold gold #E3B04B price \"Rs 3,408\" and beside it a smaller cream price with a clean strike-through line \"Rs 6,598\". Right side, a rounded gold pill with maroon text \"48% OFF\". Under all of it, small cream text: \"Pure brass Ashtalakshmi Kalash | ashopi.com\". Festive, premium, not cluttered." + SUF)

# 4. Luxury still life: the ritual kalash setup.
P['KAL4'] = PRE + ("1:1 static ad creative, 1080x1080. Template: editorial ritual still life. Photoreal, low-key warm lighting: the brass Ashtalakshmi kalash from the reference stands at centre on a red silk cloth, five fresh green mango leaves fanned in its mouth with a whole coconut wrapped in a red-and-gold thread placed on top, the traditional puja kalash setup. Around it: a small brass diya with a steady flame, grains of rice, a few rose and marigold petals, deep shadows, rich golden highlights on the engraving. "
 "Top centre, elegant large cream #F6EFE3 serif headline: \"8 LAKSHMIS.\" and on the next line in gold italic serif #E3B04B: \"One kalash.\" "
 "Bottom centre, small spaced-out cream sans-serif caps: \"DHAN  .  DHANYA  .  VIDYA  .  VIJAYA\". Luxurious, minimal, reverent." + SUF)

# 5. Real person: Diwali evening, placing the kalash in the home mandir.
P['KAL5'] = PRE + REAL + ("1:1 static ad creative, 1080x1080. Photograph at dusk inside a real Indian home: an Indian woman in her early 30s in a deep red silk saree, hair tied back, gently places the brass Ashtalakshmi kalash from the reference onto a wooden home mandir shelf, both hands around it, soft devoted smile, eyes on the kalash. Lit clay diyas on the shelf and a marigold garland, warm golden light on her face and on the engraved brass, shallow depth of field, candid and real, not posed. The kalash is clearly visible and faithful to the reference. "
 "Top-left, elegant large cream #F6EFE3 serif headline with a soft shadow for legibility: \"Lakshmi ghar aayi hai.\" Under it, smaller cream sans-serif: \"Pure brass Ashtalakshmi Kalash\". "
 "Bottom-right, small clean cream text: \"ashopi.com\"." + SUF)

for k, v in P.items():
    open(f'C:/cca/ashopi/p/{k}.txt', 'w', encoding='utf-8').write(v)
print({k: len(v) for k, v in P.items()})
