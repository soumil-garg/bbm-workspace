---
name: process-ad-creatives
description: "Ad creatives for any D2C brand: run the static-ad-creatives-maker-by-sg skill (v2, full 10-stage pipeline). Never skip research, never jump to copy."
metadata:
  type: process
---

For ANY request for ad creatives, invoke the skill `static-ad-creatives-maker-by-sg` (v2, rebuilt 2026-09-30 from the Habbits pilot). It replaces the old 8-step process and the Nano Banana Pro handoff: images are now generated in Soumil's ChatGPT Plus via Claude in Chrome.

Pipeline: intake, past Meta data, market research (Amazon + Reddit via Arctic Shift + Ad Library), psychology (segments, offers, angles, GATE 1 he picks), copy from named principles with critique (GATE 2 he approves), design in several systems, generate, QA gate, For Approval folder (GATE 3), fix loop, Meta upload with tagged ad names.

**Why:** research first, verbatim customer language beats assumptions, and he wants the same system every time. Vault plan: [[creative-testing-engine]]. Pilot log: `Projects/habbits-creative-research-oct2026.md`.

**How to apply:** call the skill, follow its stages, use his taste rules in it (headline dominant, airy layouts, offer = core promise, no invented claims). See [[feedback_creative_production_stack]], [[reference_reddit_access]], [[client_habbits]].
