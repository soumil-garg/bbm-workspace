---
name: feedback_verify_offers_live_site
description: Before ANY offer appears in an ad, re-verify it on the live website every time (shipping, discounts, popups, deadlines, review counts). Added to the static-ad-creatives skill 2026-10-01.
metadata:
  type: feedback
---

Soumil's rule: check every offer on the brand's live website, every time, before mentioning it in an ad. It is written into the skill (SKILL.md hard rule, Stage 4, QA check 8).

**Why:** On Lotus Sculpture (2026-10-01) I used "free shipping" from an old page and a cached fetch; the live banner had changed to "40% off shipping, 35% off freight". Three rounds of ads were built on the wrong offer.

**How to apply:** open the live site in a real browser (homepage banner, popups, cart, product, shipping page), log each verified offer with its page and date in the vault note, re-check at regeneration and upload. If it cannot be verified, leave it out and ask. Related: [[process_ad_creatives]].
