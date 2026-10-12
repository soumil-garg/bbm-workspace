# Design rules (hard rules for every creative)

**v3.0 note (2026-10-10):** these limits are written into each concept's body and judged by eye; no code layer enforces them any more. Rules 5, 6 and 13 were revised after the Daigo round 4 set, which Soumil loved (about 25% empty space, product 18% of the canvas, piles of forms). The manual is `whole-ad-recipe.md`.

Built from Soumil's feedback on Habbits round 1: "overfilled", "hard to focus", "headline should get the most focus", "shabby". Check every prompt and every generated image against these.

## Sources
- Pieters, Wedel & Batra (2010), "The Stopping Power of Advertising", Journal of Marketing. Eye-tracking on 249 ads: feature complexity (dense objects, text, colours) hurts attention to the brand and ad liking. Design complexity (one elaborate creative idea) helps attention and comprehension.
- Visual-critique heuristics: one primary emphasis per view; at least 1.5x size jump between hierarchy levels; no elements with equal weight but unequal importance; cut anything that does not serve the one goal.
- Meta creative best practices: one clear hero element, one headline or offer overlay, heavy text overlays lose reach.
- Breathing room is non-negotiable; nothing overlaps; limited, intentional palette.
- 60-30-10 colour rule; CRAP (Contrast, Repetition, Alignment, Proximity).
- Iyengar & Lepper (2000): too many choices freeze people. Pre-built combos reduce it.

## Hard rules
1. ONE idea, ONE focal point. The headline is the entry point.
2. Max 3 text elements (headline, optional subline, optional offer tag). Soft guide: about 12 words on the canvas, not a hard cap; never cut a word the idea needs. Data/UI formats (cart, receipt, notes) may carry more, but only as one clearly structured object. **Exception for explain creatives (top of funnel, unfamiliar category):** they may carry one definition line in addition (e.g. "It sticks your clothes to your skin."), soft guide about 18 words in total (more is fine if the idea truly needs it), but every word must earn its place, and avoid paragraphs. The definition line must be at least half the headline size and is never cut in an "overfilled" fix; cut decoration instead. What counts as an element: the headline (both lines are one element), the small supporting line, a pill or burst; numbered circles, a stamp inside the scene, the bubbles of a chat and a tape note belong to the picture and are not extra elements.
3. Headline usually 2-6 words (soft guide), understood in 1 second. No wordplay that needs decoding.
4. Headline at least 3x the size of any other text.
5. Aim for 25 to 40% empty space. The loved Daigo round 4 set sits at about 25%, his approved Swipe Desk ads at about 40%. The real test is ONE focal cluster and the headline first; if he says busy, cut elements.
6. Max 3 products in one tidy group, or a strict grid when the range itself is the message. A neatly stacked pyramid or pile of product forms counts as ONE group when volume is the message (Daigo 9 and 15). No decorative props unless the idea needs them.
7. 60-30-10 colour as a guide, not a test (the loved Daigo set put the yellow on a headline line and on a burst): background 60%, products 30%, accent 10%. The brand's accent colour (from its kit) goes on one or two elements: the offer, the pay-price or the key line of the headline.
8. One alignment axis (all centred or all left). Reading path: headline, products, offer.
9. Even, generous spacing between headline, products, offer.
10. People (only when the idea needs one; his approved ads show people in 40% and the rejected in 38%): max 2 people (a group selfie is the exception for native formats), exactly two arms/hands each, five fingers, product large and legible.
11. Squint test: blur the image; only the headline and products should still read.
12. Text sizes must be consistent in one line ("ANY 3." digits and letters same height, same baseline).
13. **Product separation (added 2026-10-04, Habbits black jar on black background):** the product must separate from its background by a measured luminance contrast of at least 3:1 (WCAG graphic-object threshold) on the product body, not just on the label. Choose the background from the product, not the other way round: dark or matte-black pack means a light, coloured or mid-tone background; if a dark mood is wanted, the product must sit in a visible light pool or against a lighter panel. A prompt line like "thin rim light so it separates" is NOT a fix: the model delivers it faintly. Decide this at Stage 5 when the look and colours are chosen. v3: on a whole-ad picture judge it by eye (the pack is lit by the scene light, has a contact shadow, separates by colour and light); measure it only where code still places the pack.

## Overfilled? Cut, do not shrink
If Soumil says overfilled: remove struck-through prices, footers, extra lines, icons, badges, cards, and props first. On an explain creative never remove the definition line (category + what it does); remove decoration first. Reduce products per card, increase padding. Count elements before and after (Habbits combos: 9 products + 10 text elements became 3 cards with 3 texts each, then 2 cards).

## Edge safety
All text and key products inside the central 84% (8% padding each edge). Meta crops Stories/Reels and Feed differently.

## Accent and palette
Take the palette ONLY from the brand kit (`brand-kit.json`, built in Stage 0 from the live site CSS and the packshots). Habbits kit: ink #111111, paper #F4F1EC, white, teal #108474; lime #C9F24B is a declared test accent only (it came from round 1, not from the brand; Soumil likes it, 2026-10-04). Yellow #FFE45C was an unapproved choice and is not in the kit. State hex codes in every prompt. Fonts: brand fonts first (Habbits: PP Mori SemiBold heading, Poppins body; wordmark from the logo file, never retyped). Anything outside the kit is flagged to Soumil as a test arm.
14. **Brand fit is three tiers, not one palette (Soumil, 2026-10-04: every ad must not look the same).** CORE never changes: logo and wordmark from the logo file, product and pack accuracy, brand fonts for brand-owned text. FLEX is the brand's extended palette (core colours plus tints and shades, packaging and site colours, neighbours) and is where variety comes from: a designed ad uses a flex background. TEST colours (outside the brand, e.g. Habbits lime) are labelled arms, at most about 25% of a round. NATIVE, UGC and real-scene lifestyle ads are exempt from the colour check because they take the colours of the real scene; they keep only product accuracy and logo rules. Checked by qa-gate check 13.
15. **Round variety (the counterweight to rule 14):** a round must not look like one ad repeated. No background family holds more than about 40% of a round (black, white, cream, teal/green, warm, etc.); at least 3 scene types in a round of 6 or more (studio product, lifestyle or real scene, native or UGC, graphic or type-led, people); at least 3 different layout archetypes (headline top, left-aligned type block, split, centre object, grid, cart or receipt object); vary photo style, camera angle and crop. Colour consistency is brand identity; layout, scene, people, mood and format are the variety axes. Checked by qa-gate check 14 and `scripts/round_diversity.py`.
