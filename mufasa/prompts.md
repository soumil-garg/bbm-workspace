# Mufasa Man OUD Deo Stick: 3-repo test prompts (28 Sep 2026)

Reference image for every generation: ref/32.jpg (Oud stick, cap off, plain background).

## REPO A: DV0x/creative-ad-agent (hook-methodology + default art-style: Anderson Clay Diorama)
Brand colors: primary #111111 (matte black), secondary #1E2A4A (deep navy), accent #B8894A (oud amber)

### A1
Type: Contrast | Source: Pain points (Amazon: "Maximum one hour freshness", "Fragrance hardly lasts a few minutes") + Value prop (24H odour control) | Target: office-goer on body spray
Hook: YOUR SPRAY QUIT AT 11 AM.
Body: Sprays sit on top of sweat and fade in an hour or two. This oud stick works on the skin, so it is still there at your 7 PM meeting.
CTA: Swap your spray
Visual world: Metamorphosis. Moment: the spray can wilting while the stick stands.

PROMPT:
Create a 1:1 social media ad image.
DIORAMA: A miniature handcrafted clay office floor seen like a museum diorama. Centre stage, on a clay desk, stands the black MUFASA MAN OUD deodorant stick from the reference image (matte black cylinder, silver lion crest, white MUFASA MAN wordmark, OUD label), rendered faithfully and upright, lit like a hero. To its left, a small generic aerosol body-spray can made of grey clay is visibly drooping and deflating, a faint grey wisp of scent evaporating from its nozzle. Behind them, three identical clay office windows, and a round clay wall clock reading 11:00. A tiny clay man in a white shirt at the next desk leans back, relaxed. The moment of change: the spray giving up while the stick holds.
LIGHTING: Split lighting, cool blue-grey from the left over the spray can, warm amber from the right over the stick. Shadow colour deep navy #1E2A4A at 30% opacity. Highlights warm cream, never pure white.
CAMERA: 35mm, dead-centre frontal, deep focus, no lens distortion.
COMPOSITION: Bisected at the centre: before state left, after state right. Background: office wall with three windows. Mid-ground: desks. Foreground: spray can and stick. Repeated elements in threes.
TEXTURE: Hero stick smooth and glossy like the real product; clay man and desk with finger-pressed texture; background flat matte; the spray can rough and institutional.
COLOR TEMPERATURE: cool left to warm right. Primary #111111 for the stick, secondary #1E2A4A for shadows and walls, accent #B8894A only on the warm light and the clock hands.
TYPOGRAPHY: HEADLINE "YOUR SPRAY QUIT AT 11 AM." top third, centred, bold condensed geometric sans-serif (Bebas Neue / Anton style), off-white #F4F1EC, ALL CAPS, tight letter-spacing. CTA "Swap your spray" bottom third, centred, medium-weight geometric sans, amber #B8894A, sentence case.
FRAMING: 10px solid #111111 border, clean edges, no vignette.
MOOD: Quiet superiority, a little wry humour. Not aggressive.
DO NOT: mannequin figures, floating objects, pure black shadows, decorative fonts, random text.

### A2
Type: Pattern interrupt | Source: Pain points (Nivea review "Excellent Against Body Odour, Poor as a Fragrance"; "don't expect the other person to smell it") + Value prop (perfume-grade oud scent) | Target: men who wear deo AND perfume
Hook: ODOUR GONE. OUD STAYS.
Body: Most deos kill the smell and leave nothing behind. This one neutralises odour and leaves a rich smoky oud that people actually notice.
CTA: Smell the difference
Visual world: Revealing. Moment: the curtain opening on the stick.

PROMPT:
Create a 1:1 social media ad image.
DIORAMA: A miniature clay theatre stage. Deep navy velvet clay curtains are being drawn open by two tiny clay stagehands on either side. Centre stage on a small plinth stands the black MUFASA MAN OUD deodorant stick from the reference image, faithful to the real product. Curling up from it, a sculpted ribbon of warm amber smoke made of glazed clay, catching the light, with tiny clay pieces of oud wood and amber resin arranged at the base in threes. In the dark wings, three tiny grey clay cartoon stink clouds shrinking away.
LIGHTING: Spotlight 45 degrees from upper-left onto the stick, rest in ambient shadow. Shadow colour #1E2A4A at 30%. Highlights warm cream.
CAMERA: 85mm, eye-level, shallow depth of field, stick sharp.
COMPOSITION: Perfect bilateral symmetry, theatre stage with wings, 3 depth layers.
TEXTURE: Stick glossy and faithful; smoke ribbon luminous glazed; curtains and stagehands finger-pressed clay; stink clouds rough and dull.
COLOR TEMPERATURE: Neutral dark scene, the amber smoke is the only saturated element (#B8894A).
TYPOGRAPHY: HEADLINE "ODOUR GONE. OUD STAYS." top third, centred, bold condensed geometric sans, off-white #F4F1EC, ALL CAPS. CTA "Smell the difference" bottom third, centred, amber #B8894A, sentence case.
FRAMING: 10px solid #111111 border.
MOOD: A reveal. Premium, theatrical, confident.

### A3
Type: Social proof | Source: Testimonials (site review: "Finally a deo stick that doesn't leave white marks." Rohan, Delhi) + Pain points (Amazon: "It will stain ur clothes") | Target: men who wear dark shirts
Hook: "FINALLY. NO WHITE MARKS."
Body: No chalky streaks on your black shirt, no sticky roll-on that takes five minutes to dry. Swipe, dress, go.
CTA: Wear black again
Visual world: Celebration. Moment: pulling on a black shirt, spotless.

PROMPT:
Create a 1:1 social media ad image.
DIORAMA: A miniature clay tailor's wardrobe. A tiny clay man with an expressive happy face is mid-motion pulling on a crisp black shirt, arms raised, the underarm area of the shirt visibly spotless. Behind him, three black shirts hang in a perfect row on a clay rail. On a small clay dresser in the foreground stands the black MUFASA MAN OUD deodorant stick from the reference image, faithful to the real product. A small clay mirror reflects him grinning.
LIGHTING: Golden hour, warm directional from frame-right, amber-touched edges. Shadow colour #1E2A4A at 30%. Highlights warm cream.
CAMERA: 35mm, bird's-eye tilt 15 degrees down, deep focus.
COMPOSITION: Centred subject framed by the wardrobe doors on both sides, shirts repeating in threes.
TEXTURE: Man and shirts finger-pressed clay; stick glossy and faithful; wardrobe walls flat matte.
COLOR TEMPERATURE: Warm throughout, amber accent glowing. Primary #111111 shirts and stick, navy #1E2A4A walls.
TYPOGRAPHY: HEADLINE "FINALLY. NO WHITE MARKS." top third, centred, bold condensed geometric sans, off-white #F4F1EC, ALL CAPS. Small line under it "Rohan, Delhi" in medium sans. CTA "Wear black again" bottom third, amber #B8894A.
FRAMING: 10px solid #111111 border.
MOOD: Relief and quiet pride.

## REPO B: krusemediallc/arcads-claude-code (chatgpt-image-ad + prompt library + 3 safety suffixes)

SUFFIXES appended to every prompt:
[NO PLATFORM CHROME] Render only the standalone ad creative (the static image uploaded to Meta), not a screenshot of how it displays in-feed. Exclude device chrome, Sponsored labels, captions, engagement rows, buttons. Just the standalone image.
[EDGE-SAFE] All text, headlines, table content, and the product must fit within the central 84% of the canvas (about 8% padding from every edge). Backgrounds may bleed; text and focal elements may not touch or run off any edge.
[TEXT FIDELITY] Inside body-text blocks: plain words only, no emoji, no special glyphs mid-sentence. Render the exact number of rows and items specified, do not invent extra ones.

### B1 (template T37 Weather-app forecast UI)
Insight: smell fades in 1 to 2 hours; "humid hot sweaty" Indian days; claims like 48h/72h are distrusted.
PROMPT:
1:1 static ad creative, 1080x1080, edge-to-edge. A fake weather-app forecast UI styled as "your day on the Mufasa Man Oud Deo Stick". Standalone ad creative. Background deep matte black #111111 with a very subtle warm amber glow at the centre.
Top section (about 22% height): a small muted grey caps label "TODAY, MUMBAI", then below a centred bold off-white sans-serif headline in two stacked lines: "36°C. 80% Humidity." / "0% Sweat Smell."
Below the headline, a thin grey hairline divider.
Middle section (about 44% height): a horizontal hourly forecast strip, five evenly spaced columns, each top to bottom: time label (small grey sans), a small minimal vector-style icon in soft amber, a condition label in off-white sans, a smaller subtitle in light grey. Columns:
Column 1: "9 AM" sun icon "Metro Crush" "Fresh"
Column 2: "12 PM" cloud icon "Humid Front" "Still fresh"
Column 3: "3 PM" thermometer icon "Meeting Heat" "No odour"
Column 4: "7 PM" dumbbell icon "Gym Session" "Holding"
Column 5: "10 PM" moon icon "Dinner Date" "Smoky oud"
(Render icons as simple vector shapes, not emoji.)
Lower section (about 30% height): the MUFASA MAN OUD deodorant stick from the reference image, cap off beside it showing the white balm, centred, premium studio product photography, soft rim light, faithful to the real label.
Bottom (about 4%): small off-white sans text "Mufasa Man Oud Deo Stick  |  mufasaman.com"
Modern minimal premium aesthetic. [suffixes]

### B2 (template T6 Comparison table, dark, hooky)
Insight: sprays "last a few minutes to 2 hours", re-buy often; roll-ons "sticky, takes minutes to dry"; people want odour control AND a scent.
PROMPT:
1:1 static ad creative, 1080x1080, edge-to-edge. A dark-mode comparison ad image. Near-black background #0E0E10 with a subtle radial warm amber #B8894A glow at the centre. Tiny amber "+" marks in the four corners.
Top text in chunky off-white sans-serif, stacked two lines centred: "Your Body Spray" on line 1, "Quits By Lunch" on line 2, where the word "Lunch" is coloured amber #D4A25A and the rest off-white.
Below, a row of three rounded-square tiles: left tile dark grey with a simple white outline of a generic aerosol can and caption "Body Spray"; middle a small angled amber "VS" badge; right tile black with the MUFASA MAN OUD deodorant stick from the reference image and caption "Mufasa Oud Stick".
Below the tiles, a dark comparison table with thin grey grid lines, header row in grey caps: "WHAT YOU GET" | "BODY SPRAY" | "OUD STICK". The OUD STICK column outlined with a thin amber border. Exactly 5 rows:
"Scent lasts" | "1-2 hours" | "All day"
"Odour" | "Covers it" | "Neutralises it"
"Alcohol" | "Yes" | "0%"
"Where it goes" | "Half in the air" | "All on skin"
"One pack lasts" | "Weeks" | "Months"
Brand column values in amber, others in grey. Numbers in monospace. [suffixes]

### B3 (template T32 Pain-point checklist + product)
Insight: all five items are paraphrased consumer complaints from Amazon reviews.
PROMPT:
1:1 static ad creative, 1080x1080, edge-to-edge. A clean editorial layout. Warm off-white background #F4F1EC.
Top section (about 22% height): centred bold black sans-serif headline, two stacked lines, large: "SMELL GONE" / "BY LUNCH?"
Middle section (about 34% height): exactly five checklist rows, each a hollow grey square checkbox and text in regular black sans-serif:
Re-spraying in the office washroom
Scent that fades in an hour
Sticky roll-on that never dries
White marks on your black shirt
Buying a deo AND a perfume
Lower section (about 30% height): the MUFASA MAN OUD deodorant stick from the reference image with its cap off showing the white balm, a few pieces of dark oud wood beside it, soft natural light, premium product photography, faithful label.
Bottom section (about 14% height): line 1 bold serif "ONE SWIPE. OUD ALL DAY."; line 2 smaller sans "Mufasa Man Oud Deo Stick. Alcohol-free, aluminium-free, no white marks. mufasaman.com"
Modern, premium, calm. [suffixes]

## REPO C: keith-wohnv/Static-Ads (Brand DNA modifier + 50-template library + TOF/MOF/BOF copy)

BRAND DNA IMAGE MODIFIER (prepended):
Premium Indian men's grooming brand Mufasa Man. Matte black cylindrical deodorant stick with a silver lion-crest emblem, white MUFASA MAN wordmark, tagline BOLD. BRILLIANT. CLASSIC. and OUD label. Palette: matte black #111111, deep navy #1E2A4A, warm oud amber #B8894A, off-white #F4F1EC. Clean modern sans-serif headlines with an elegant serif accent. Soft directional studio light, warm shadows, smoky oud wood and leather props. Mood: understated masculine luxury.

### C1 (template 7 Us vs Them)
PROMPT:
[modifier] Use the attached image as brand reference and match the exact product design. Create: a side-by-side comparison divided vertically. Left: muted grey-blue background. Right: matte black #111111 background. Centre top: white circle with "VS". Left header: "BODY SPRAY" with a generic unbranded grey aerosol can, and a list with red X marks: "Fades in 1-2 hours", "Masks smell, doesn't stop it", "Alcohol that stings", "Half of it goes in the air", "Re-buy every month". Right header: "MUFASA MAN OUD STICK" with the black Mufasa Man Oud deodorant stick from the reference, and a list with amber check marks: "Lasts all day", "Neutralises odour", "0% alcohol, 0% aluminium", "Every swipe on skin", "One stick lasts months". MUFASA MAN wordmark bottom right.

### C2 (template 16 Curiosity Gap / Hook Quote Testimonial)
Uses a real verified Amazon review of the Oud stick.
PROMPT:
[modifier] Use the attached image as brand reference and match the exact product design. Create: a static ad on a clean off-white #F4F1EC background. Top centre: large amber #B8894A opening quotation marks. Below: mixed-weight headline in black: first line in italic serif "The fragrance is very premium,", next two lines in enormous heavy bold all-caps sans-serif "BOLD AND CLASSY.", followed by a smaller sentence-case line "A proper rich oud smell. And it's a deodorant." Closing quotation marks and "Verified Amazon buyer" in regular weight. Left side bottom third: the Mufasa Man Oud deodorant stick at a slight angle, cap off showing the white balm. To the left of the product: a small round badge "0% Alcohol, 0% Aluminium". Right side bottom third: five filled amber stars and bold text "Oud Deo Stick, 75g". Bottom edge: small text "Individual experiences may vary."

### C3 (template 40 Native / Ugly Post-It Note)
PROMPT:
[modifier] Use the attached image as brand reference and match the exact product precisely. Create: a lifestyle product photo on a cluttered Indian office desk, afternoon light through blinds. Frame slightly off-centre, feels found rather than composed, slight sensor grain. Centre: the Mufasa Man Oud deodorant stick on the desk next to a laptop, a steel tiffin box and a cutting-chai glass, slightly angled. A few paper clips and a pen around the base. Stuck on the product: a yellow square post-it note, slightly crooked, realistic paper texture with a crease, handwritten in thick black marker, imperfect lowercase: "stop re-spraying" / "in the office loo" / "1 swipe at 8am" / "still oud at 8pm". No logo overlay; brand carried by the packaging. Bottom: small caption text "mufasaman.com, the deo that smells like perfume".
