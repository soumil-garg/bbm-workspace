---
name: brand-kit-required
description: Brand kit has core/flex/test tiers; native ads exempt; rounds must stay visually diverse (check 14)
metadata:
  type: feedback
---

Soumil (2026-10-04) asked whether brand colours were being used for Habbits. They were only partly: lime #C9F24B and yellow #FFE45C were Claude's choices, not the brand's; fonts were not brand fonts. He approved Habbits teal #108474 (from habbits.in CSS) AND lime as a declared test accent.

**Why:** off-brand colours and fonts make client ads look unlike the brand; the old rule was one sentence with no step behind it.
**How to apply:** Stage 0 runs scripts/brand_kit.py extract and curates kit/brand-kit.json; Stage 5 palette and fonts only from the kit (layouts use "kit" and $tokens); QA check 13 runs brand_kit.py check. Habbits kit: C:\cca\habbits\kit\brand-kit.json. See [[process_ad_creatives]], [[client_habbits]].

**Correction (same day):** Soumil: brand-kit-only would make every ad look the same; he wants diversity. Kit is now three tiers (core identity, flex extended palette, test colours capped ~25% of a round), native/UGC/real-scene ads are exempt from the colour check, and QA check 14 (scripts/round_diversity.py) enforces round variety (no background family over 40%, 3+ scene types, 3+ layout archetypes). See [[feedback_tof_unaware]] for why native matters.
