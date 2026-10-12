---
name: reference-whole-ad-generation-recipe
description: "How Daigo round 3 (10 Oct 2026) made 13 whole-ad creatives: real pack refs (clean pouch + branded sachet) to the OpenAI edits endpoint, prompt = refs + construction brief + concept + avoid; scripts, cost, what failed"
metadata:
  node_type: memory
  type: reference
  originSessionId: b3607133-6288-42df-85dd-d0d6d53e5a58
  modified: 2026-10-10T12:30:04.949Z
---

**v3.0 update (10 Oct, late):** the recipe is now the skill itself: `references/whole-ad-recipe.md`, generic scripts `whole_ad.py`, `deliver_ads.py`, `make_copy_inputs.py`, the gold config `references/templates/ads_config.example.json` (rebuilds the 13 round 4 prompts byte for byte). This note is only the round 3 origin; see [[feedback-round4-loved-recipe]].

Scripts `C:\cca\daigo\round3\` (copy in the skill `references/examples/daigo_round3/`): `build_round3.py prompts|gen [IDs] [--tag _vN]`, `concepts_round3.py` (the concept dictionary C), `sheet_round3.py` (numbered contact sheet, args `out.jpg W cols NUMBER:ID:label ...`), `final_key.json`.

**Prompt anatomy (assembled in this order):** ROLE_REFS (image 1 = real pouch, image 2 = real sachets, what they look like, no added badge or claim, physically in the scene with contact shadows) + ART (finished 4:5 poster in the construction style of approved ads: one focal point, max three brand hues plus white, designed colour field or built studio set, soft studio light, three-level type, one headline treatment, margins in the central 84%, exact spelling) + the concept body (headline text, background, hero, light, supporting line, first headline line at least 9% below the top) + NEG (pasted look, flat cut-outs, plain or square sachets, extra logos, invented or health claims, unspecified text, readable text on background objects).

**Settings:** `gpt-image-2.5-sunburst`, `gen_image.py` edits endpoint with `--ref` pouch and `--ref` sachet, size 1024x1280, 5 parallel workers, about $0.055 to $0.066 an image (13 finals plus 4 replaced plus 3 reference builds = $1.30). The pouch reference is the real photo with the badge, seal and icon row removed by the model itself (prompt `p_clean_pouch.txt`); the sachet reference is generated from that pouch (`p_sachet_ref.txt`).

**What worked:** typeset Hinglish headlines and chat text exact on 12 of 13 ads (the handwritten tape note lost a capital); branded slim sachets every time once a sachet reference was passed; the model puts the pouch in the scene with believable shadows and condensation; hands plausible.

**What failed and the fix:** head covering a headline word (put the whole headline above the head); book spines and a DHABA signboard in the background (add "no readable text on background objects"); handwriting lost a capital ("Ki" with a lowercase i, say "every letter a capital letter"); a plain-sachet prompt produces condom-pack squares.

**Limits:** the sachet front is derived from the pouch, not from a photo of the real sachet; ask the client for one. On 10 Oct the API returned credit_balance_exhausted: the ledger (`C:\cca\_ledger\balance.json`, a manual estimate) said there was credit left, so check the OpenAI billing page when a run is big.
