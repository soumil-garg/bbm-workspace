# Copy principles (Stage 4)

Every headline and primary text must be built from these, and labelled.

| Principle | Source | How to apply |
|---|---|---|
| Match copy to awareness and how many claims the buyer has heard | Schwartz, Breakthrough Advertising | see psychology-framework |
| Headline types: self-interest, news, curiosity | Caples, Tested Advertising Methods | label each headline with its type |
| Be specific, give a reason why | Hopkins, Scientific Advertising; Ogilvy | "Rs 249 product, free" beats "great deal"; say why |
| People comply more when given a reason | Langer 1978 ("because") | "The 3rd is free, because one product never fixes it" |
| FREE pulls far harder than a small price | Shampanier, Mazar & Ariely 2007 | lead with FREE / Rs 0, not "33% off" |
| Above Rs 100 a rupee amount feels bigger than a percentage | Berger, Contagious (rule of 100) | show rupees saved, not percent |
| Anchoring and loss aversion | Kahneman | show the full price then what they pay; frame skipping as losing the free item |
| Mental accounting | Thaler | the free item feels like a gift, so gifting/sharing angles work |
| Social proof, authority, scarcity, reciprocity, unity | Cialdini, Influence | ONE lever per ad, labelled |
| Value equation: result x likelihood / (time x effort) | Hormozi, $100M Offers | raise likelihood (routine, proof) and cut effort |
| Customers' own words | Joanna Wiebe, Copyhackers | headlines lifted from review/Reddit phrases |
| Every line pulls into the next | Sugarman, Adweek Copywriting Handbook | primary text as one continuous slide |
| Pratfall: admitting a limit builds trust | Aronson 1966 | "No, it won't work in 1 day" for sceptical audiences |
| Too many choices freeze | Iyengar & Lepper 2000 | pre-built combos before "pick any" |

## Label template (per creative)
```
### <ID> (<offer>) <name>
Headline: <2-6 words> | Sub: <line> | Alts: <2>
Primary (short): ...
Primary (long): ...
Meta headline: ...
Labels: awareness / headline type / lever / origin: SOURCED (quote + where) or PATTERN-DERIVED (pattern + count) / reason-why
Image idea: one line; read headline + picture idea as one message (a rule: headline first, picture second, together one story that proves the idea and shows the product taking part)
Claims used: register rows (claim | brand property where found | URL | verified | date)
Cold read: what a person who has never heard of this product would think the line means, written from the headline and subline alone
```

## Rules
- One idea per ad. 2-6 word headline. Customers' words over marketing language.
- The offer must be understood in under 2 seconds.
- Verify every price on the live site; compute totals and anchors yourself; state the cart rule (Habbits: cheapest item free).
- On top-of-funnel copy for an unfamiliar category the subline defines the product (category + what it does, e.g. "Body glue sticks clothes to your skin."), it does not repeat a claim ("holds up to 8 hours" is a claim, not a definition). Claims come after the definition.
- Timelines are the brand's "what to expect", never fabricated customer testimonials. Only real reviews, attributed as the source shows.
- Brand-used claims ("3X whiter in 30 days", "10,000+ customers") are NOT reusable on the brand's say-so alone: each must be found on a brand property (site, pack, listing, certificate, test report) and sit in the claim register; otherwise remove it or get Soumil's explicit, logged acceptance of the risk (Stage 4b). Timeframe-and-outcome claims also face Meta's unrealistic-outcome rule (policy checklist row 3).
- Meta policy: the full pre-check is `policy-checklist.md`; at minimum no pointing at viewer attributes (first person or about the product/habit), no negative self-perception about appearance or hygiene, no outcome-within-a-timeframe promise without a qualifier.
- Published-content style: no em-dashes, no asterisks in ad text.
- Bilingual brands (Soumil, 2026-10-10): offer both Hinglish and English lines for every picture and run roughly half and half; his approved headlines are mostly English (contrast, exaggeration, a joke, a question, a concrete number) and a Hinglish-only round drew the complaint.

## Critique pass (independent second reader)
The author never grades their own copy. A second reader (a separate agent with a fresh context) gets: the copy table (headline, sub-line, primary text, Meta headline), the one-line image idea, the claim register rows with sources, the segment and awareness level from the ICP card, the policy checklist, and the competitor headlines from the sweep. It does NOT get the author's labels or reasoning, so it cannot be talked into a verdict. `scripts/make_copy_inputs.py --extra <file.md>` carries those extra inputs (competitor headlines, claim register rows, policy rows, awareness level, cold reads). It returns, per creative:
1. **Cold read in its own words:** what it thinks is being sold and what the line means (stranger read). Wrong, blank or "no idea" on top-of-funnel copy for an unfamiliar category is a fail.
2. **What a sceptic would say:** the strongest objection or "that is fake" reaction, quoted.
3. **Claims without proof:** any claim, number or implied promise not in the register or not backed by its source.
4. **Policy flags:** any row of the policy checklist the copy or image idea trips, with the rule named.
5. **Sounds like a competitor:** the closest competitor line and why, if it is close.
6. **Headline-image pair:** whether the headline plus the image idea give curiosity or value together, or whether one undermines the other (a rule: a pair that does not tell one story fails).
7. **Scores** (the 1 to 5 rubric a to f in `references/templates/critic_template.md`; "scroll-stop" is an opinion, not a measurement).
8. **Double-meaning and slang screen** (a separate native Hindi and Hinglish reader, added 2026-10-10): flags crude or sexual double meanings, regional slang, political, religious, alcohol or rule-breaking readings per line and per line plus picture, with severity and a safe rewrite; HIGH and MED fail.
The author rewrites what fails and records what changed. Table goes into the vault note.

## Bottom-funnel copy
Offer is the headline. Show the mechanism ("ADD ANY 3. ONE GOES Rs 0."), the range, real prices. No pain agitation. Ask for an end date: real urgency is the strongest missing lever, never invent one.
