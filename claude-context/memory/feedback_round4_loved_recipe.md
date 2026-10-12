---
name: feedback-round4-loved-recipe
description: "2026-10-10: Soumil loved ALL 15 Daigo round 4 creatives and told me to remember how and make the skill give the same output every time; the recipe, what v3.0 removed, where it lives"
metadata:
  node_type: memory
  type: feedback
  originSessionId: b3607133-6288-42df-85dd-d0d6d53e5a58
  modified: 2026-10-10T14:50:23.468Z
---

On 10 Oct 2026, after Daigo round 4: "You've finally done a very, very good job, and I know it took multiple iterations ... I finally love the output. I love each and every one of the creatives ... Remember how you did that, and update the skill in such a way that the things I did not like, you remove them, and it gives us a similar output every time I call the skill."

**The recipe that earned it (now the skill's default, v3.0):**
1. Real references: the real pack photo with banned badges removed by the model, plus a branded reference for every product form (sachet); plain or square forms read as condom packs.
2. Lines first, both languages (9 English, 6 Hinglish), an independent critic AND a separate native-reader slang screen, the claim register and policy check, and he approves the lines as text before any image exists.
3. The image model draws the WHOLE ad in one pass (scene, pack, forms, headline, small line, badge) from the references with one prompt anatomy: reference roles + construction brief + concept + avoid list.
4. One story per picture (line says it, picture proves it, product takes part); poster look with a headline treatment and a concrete number or joke.
5. QA at zoom (spelling, hands, background text, product forms), self-check against his approved ads, numbered sheets plus the exact prompts delivered, a short message with the key, cost, what is not clean and five picks.
Cost: about $0.066 a picture, 13 new pictures $0.86.

**What v3.0 removed from the skill:** the code text layer and pack cut-outs as the default (render_ad.py is now an edit tool only), the die-cut tile, the measured product-separation check as the main check, Hinglish-only, lines written from the claims-safe list, the "real people" taste belief, the hard 40% empty-space rule (the loved set sits at 25%), design-system prompts as the driver.

**Where it lives:** the skill `static-ad-creatives-maker-by-sg` (v3.0: SKILL.md, `references/whole-ad-recipe.md`, `scripts/whole_ad.py`, `deliver_ads.py`, `make_copy_inputs.py`, `references/templates/`, gold outputs in `references/examples/daigo_round4/`); backup of the old skill `Vault/Archive/skill-backups/static-ad-creatives-maker-by-sg.before-v3-2026-10-10.zip`; vault `Projects/ad-skill-v3-whole-ad-oct2026.md`.

**Audit (same evening):** a fresh agent simulated a run on another brand and found 64 problems (the QA gate failed the loved set, leftover claims-safe and soft-harmony instructions, Daigo leaking into new configs, a Hinglish-only copy gate); all fixed and re-tested. The skill now has a blank config skeleton, `references/legacy/` for rejected approaches, and an acceptance test: the Daigo round 4 set must pass the QA gate.

**How to apply:** on any ad creative request call the skill and follow the manual; do not improvise a new method. The honest open test is a second brand (Habbits is next in line): run v3 end to end there, report what needed adapting, and fix the skill, never the output by hand. Ask before pushing the skill to GitHub. See [[process-ad-creatives]], [[reference-whole-ad-generation-recipe]], [[feedback-whole-ad-generation-harmony]], [[feedback-daigo-copy-both-languages-double-meaning]].
