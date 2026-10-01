# QA gate (Stage 7)

Run on EVERY generated image before Soumil sees anything. Build a contact sheet (`scripts/contact_sheet.py`), view it, then zoom into people, small text, prices and labels (crop with PIL and view). Fail any single item = regenerate or local fix.

## The 11 checks
1. Thumb-stop: would it stop the scroll?
2. 2-second read: offer and promise clear in 2 seconds?
3. One idea only.
4. Headline dominant, fully legible, spelled exactly as specified.
5. Product accurate: labels, colours, sizes, SKUs match the reference. No invented label text, no wrong ml/grams.
6. Anatomy: hands (5 fingers), faces, limbs.
7. Nothing important in the edges (84% safe area).
8. Claims real: no invented stats, prices match the live site.
9. Looks different from the other creatives in the set.
10. Looks different from competitor ads.
11. **Stranger test (every top-of-funnel image, and any image for an unfamiliar category):** cover everything you know about the product and read only the image as someone who has never heard of this product type. Write down two answers: "what is being sold?" and "what does it do / what problem does it solve?". If either cannot be answered from the image alone, fail it. Log the cold read next to the image in the vault note.

## Known failure modes (seen so far)
| Failure | Cause | Fix |
|---|---|---|
| Props from the reference appear (grapefruit, mint, charcoal, paste smears, badges) | reference photo contains props | packshot-only reference; add "show ONLY the product containers, no props from the reference" |
| Offer label too small | model shrinks secondary text | say "large, about as big as the top caption" |
| American-looking props (red plastic cups) | model default | specify local props (steel chai glasses, kulhad) |
| Stray extra person/arm | model | regenerate; state exact counts |
| Wrong text in chat bubbles / extra messages | emoji, invented rows | plain words only, exact count of messages |
| Mixed text sizes in one line ("ANY 3.") | model | local recompose in PIL with matched heights and baseline |
| Product label drift (250 ml became 500 mL, 100 g became 50 g) | model | check every label; regenerate |
| Reference sheet leaks a badge ("As seen on") | badge in the packshot | crop it out of the reference |
| Overfilled layout | too many elements | cut elements (design-rules) |
| Hook ad that only works if you already know the product ("Tape came off in 10 minutes?", "Dance. Don't adjust.") | reviewer knows the product, image never defines it | add the definition line (category + what it does), or relabel the ad middle-of-funnel |

## Log
Record in the vault note: N passed first time, which were regenerated and why, what to change next time. Keep failed files in `rejected\`.
