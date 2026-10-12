# QA gate (Stage 7)

Run on EVERY generated image before Soumil sees anything. Build the QA sheets (`python scripts/whole_ad.py qa --config ...`), view them, then zoom into people, small text, prices and labels (crop with PIL and view). Fail any single item = regenerate with the sentence that caused it patched (or a local fix on a finished picture). v3: the 14 checks below PLUS the whole-ad checks A to H.

## Which checks bind in v3
Binding: checks 1 to 11 and 14 (14 by eye plus `round_diversity.py`), the whole-ad checks A to H below, and check 8 (offers re-verified on the live site, manual). Check 12 is judged by eye, check 13 is advisory. ACCEPTANCE TEST for any change to this gate or to its scripts: the Daigo round 4 set (`references/examples/daigo_round4/gold/`, pictures in `Desktop\Daigo Ads\Round 4\For Approval`) must still pass it (it does: `round_diversity.py` PASS at 33% warm neutral; `brand_kit.py check --tolerance 60 --advisory` no FAIL).

## The 14 checks
1. Thumb-stop: would it stop the scroll?
2. 2-second read: offer and promise clear in 2 seconds?
3. One idea only.
4. Headline dominant, fully legible, spelled exactly as specified.
5. Product accurate: labels, colours, sizes, SKUs match the reference. No invented label text, no wrong ml/grams.
6. Anatomy: hands (5 fingers), faces, limbs.
7. Nothing important in the edges (84% safe area).
8. Claims real: no invented stats, prices match the live site. **Every offer in the image or copy (shipping, discount, deadline, guarantee, review count) was re-verified on the live website today, with the source page logged in the vault note.** An offer that was not re-checked fails this item.
9. Looks different from the other creatives in the set.
10. Looks different from competitor ads.
11. **Stranger test (every top-of-funnel image, and any image for an unfamiliar category):** cover everything you know about the product and read only the image as someone who has never heard of this product type. Write down two answers: "what is being sold?" and "what does it do / what problem does it solve?". If either cannot be answered from the image alone, fail it. Log the cold read next to the image in the vault note.
12. **Product separation (v3: by eye).** On a whole-ad picture the pack separates from its background by colour and light: lit by the scene light, standing on a surface with a contact shadow, nothing that reads as a cut-out (whole-ad check A). Dark and navy grounds work with a blue pack when the pack carries its own light and a lit edge (Daigo 9, navy ground, loved). Measure the luminance ratio only where CODE places the pack (a v2-style edit): sample the PLAIN colour band of the pack against the strips left, right and above it, ratio `(max(L1,L2)+0.05)/(min(L1,L2)+0.05)` with relative luminance (`f=lambda v:v/255/12.92 if v/255<=0.03928 else ((v/255+0.055)/1.055)**2.4`), at least 3:1.
13. **Brand fit (designed ads only):** `python scripts/brand_kit.py check <brand-kit.json> <image> --tolerance 60 --advisory` against the core and flex tiers (v3: advisory, because a generated picture is lit by its scene and the model never renders a kit hex exactly; the strict version failed 2 of the 15 loved Daigo pictures. Look at every REVIEW and worry only about a ground of a clearly different hue family). FAIL = a background or large area (20%+) outside both tiers; REVIEW = a 5%+ area off-kit (product photography and test-accent tints can be legitimate, look at it). Test accents pass only inside a labelled test arm (cap about 25% of a round). Native, UGC and real-scene ads are exempt (`--native`): check product accuracy and logo only. The headline face is the heavy condensed grotesque of the construction brief (a brand typeface survives only inside the wordmark that comes from the pack reference); the logo and wordmark come from the pack reference. Habbits C4 (yellow #FFE45C background) fails.
14. **Round variety:** `python scripts/round_diversity.py <round>/out` (or the For Approval folder; contact sheets are skipped; it errors on 0 images): no background family over 40% of the round, no near-duplicate pairs; then by eye at least 3 scene types and 3 layout archetypes in a round of 6 or more. A round that passes check 13 on every image but fails check 14 is not done: loosen colours within the flex tier, change scenes, add native ads.

## Whole-ad checks (v3.0, 2026-10-10: add these to the 14; fail any one and regenerate)
A. **Pasted test:** at full size, does anything look cut out, floating, flat-lit or lit from a different direction than the scene? The pack, the forms and the props must stand, lean, lie or be held with contact shadows.
B. **Harmony test:** read the line with the picture covered, then the picture with the line covered. They must tell ONE story and the product must take part in it. A picture that merely repeats the words is a weak pass at best; one that contradicts them fails.
C. **Product-form test:** every pack and form (sachet, stick pack, jar, tube) matches its reference: shape, ends, print, every printed word spelled right; nothing plain, square or unbranded; no badge, seal, icon or claim the reference does not carry.
D. **Text exactness at zoom:** crop every headline, small line, badge, chat bubble and tape note and tick off each string in the concept's `texts` letter by letter (apostrophes, commas, full stops, the count of stretched letters and exclamation marks, capitals in handwriting).
E. **Hands and bodies:** five fingers, two arms, no extra limbs, hands that grip the object plausibly; no person or hand covers a headline word.
F. **Background text:** no readable text on any background object (book spines, signboards, labels, screens, lanyards) except what the concept specifies.
G. **Slang screen done:** the line is in the native reader's output as PASS, or its MED and HIGH flags were fixed; the picture follows the picture-safety list (`hinglish-never-use.md`, `whole-ad-recipe.md` section 7).
H. **Round mix:** the language split (about half and half for a bilingual market), at least 3 scene types and 3 layouts, no ground family over about 40%, one native slot, one loud or funny slot.
Then run `python C:\cca\inspiration\swipe\construction_selfcheck.py <label> <pictures>` and report the gap against his approved ads (clean finish 83%, soft studio light 77%, flat or studio ground 52%, the picture demonstrates the idea 71%, a type effect 43%, product 12% of the canvas, empty space 40%). Daigo round 4: 87, 67, 40, 73, 87, 18 and 25.

## Known failure modes (seen so far)
| Failure | Cause | Fix |
|---|---|---|
| Props from the reference appear (grapefruit, mint, charcoal, paste smears, badges) | reference photo contains props | packshot-only reference; add "show ONLY the product containers, no props from the reference" |
| Offer label too small | model shrinks secondary text | say "large, about as big as the top caption" |
| American-looking props (red plastic cups) | model default | specify local props (steel chai glasses, kulhad) |
| Stray extra person/arm | model | regenerate; state exact counts |
| Wrong text in chat bubbles / extra messages | emoji, invented rows | plain words only, exact count of messages |
| Mixed text sizes in one line ("ANY 3.") | model | regenerate with the sentence patched; a local PIL recompose only on a FINISHED picture Soumil already approved |
| Product label drift (250 ml became 500 mL, 100 g became 50 g) | model | check every label; regenerate |
| Reference sheet leaks a badge ("As seen on") | badge in the packshot | crop it out of the reference |
| Overfilled layout | too many elements | cut elements (design-rules) |
| Hook ad that only works if you already know the product ("Tape came off in 10 minutes?", "Dance. Don't adjust.") | reviewer knows the product, image never defines it | add the definition line (category + what it does), or relabel the ad middle-of-funnel |
| A head or hand covers a headline word (Daigo round 3, MAT) | the person stands high in the frame | put the whole headline ABOVE the head and the person lower |
| Readable text on background objects (book spines, a DHABA signboard) | the model fills scenes with signage | "no book spines, titles or labels anywhere", "no signboards" in the concept, plus the avoid item |
| A handwritten note loses a capital ("Ki") | the model | "every letter a capital letter and no lowercase letter anywhere" |
| Plain square sachets (the condom-pack look) | no form reference, or the word "plain" in the prompt | pass the form reference, the form rule sentence, never write plain |
| White powder cloud or white splash | the model | a pale drink in a steel tumbler, a tidy stack, the avoid item |
| An unlabelled clear bottle in a car boot | the model | the brand's shaker or a labelled bottle, a parked car, nobody inside |
| The pasted look | pack or text composited over a scene | whole-ad generation only |
| A banned badge, seal or icon appears on the pack | the reference photo carried it | the cleaned pack reference |

## Log
Record in the vault note: N passed first time, which were regenerated and why, what to change next time. Keep failed files in `rejected\`.
