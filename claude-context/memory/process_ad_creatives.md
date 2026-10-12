---
name: process-ad-creatives
description: "Ad creatives for any D2C brand: run the static-ad-creatives-maker-by-sg skill (v3.0, whole-ad pipeline, the method Soumil loved on Daigo round 4). Lines first in both languages with a slang screen, then the image model draws the WHOLE ad from real references. Never paste, never skip research."
metadata:
  node_type: memory
  type: process
  originSessionId: b3607133-6288-42df-85dd-d0d6d53e5a58
  modified: 2026-10-10T14:50:15.412Z
---

For ANY request for ad creatives, invoke the skill `static-ad-creatives-maker-by-sg` (v3.0, rebuilt 2026-10-10 after Daigo round 4). The manual for the copy and image steps is its `references/whole-ad-recipe.md`; the scripts are `whole_ad.py`, `deliver_ads.py` and `make_copy_inputs.py`; the gold config `references/templates/ads_config.example.json` rebuilds the 13 Daigo round 4 prompts byte for byte. Images go through the OpenAI API (not ChatGPT in Chrome).

Pipeline: intake, past Meta data, market research, psychology (GATE 1 he picks), lines in BOTH languages with an independent critic, a native-reader slang screen, the claim register and the policy check (GATE 2 he approves the lines as plain text, before any image), concepts and references, the model draws the whole ad (`whole_ad.py gen`), QA by eye and zoom plus the self-check, deliver (`deliver_ads.py`: numbered sheets, exact prompts; GATE 3 his picks), fix loop, upload only after his yes (paused, UTMs, Dropbox, AI label).

**Why:** on 10 Oct 2026 Soumil said "You've finally done a very, very good job ... I love each and every one of the creatives ... update the skill ... so it gives us a similar output every time I call the skill." Before that he rejected pasted compositing, plain sachets that looked like condom packs, flat claims-safe copy, Hinglish only and a controversial verb trio ([[feedback-round4-loved-recipe]]).

**How to apply:** call the skill, read `whole-ad-recipe.md`, obey the Never list at the top of SKILL.md, do not improvise a new method. Related: [[reference-whole-ad-generation-recipe]], [[feedback-daigo-copy-both-languages-double-meaning]], [[reference-openai-key-rotation]], [[feedback-whole-ad-generation-harmony]]. Vault plan: [[creative-testing-engine]]; v3 changelog: `Projects/ad-skill-v3-whole-ad-oct2026.md`.
