---
name: research-depth-minimums
description: Minimum research volume for the ad creative skill: 1,500+ Amazon reviews (60%+ critical), 15+ competitor brands with images
metadata:
  type: feedback
---

Soumil (2026-10-04): 25 reviews per product is too thin to see a pattern. Pull at least 1,500 Amazon reviews per brand run, at least 60% 1-3 star, because the most negative reviews are where customers list their real concerns; count themes, not just quotes. Competitor ads: at least 15 brands (more in crowded markets), up to 30 active ads each, look at the IMAGES (numbered sheet per brand), tag bucket/offer/hook/format with run length.

**Why:** small samples hide patterns; text-only competitor reads miss what the creative actually looks like.
**How to apply:** Stage 2 of [[process_ad_creatives]]; script scripts/competitor_sweep.py; bucket set is the 7 in the vault note competitor-sweep-oct2026.

**2026-10-09 failure and fix (Daigo):** I judged competitors by Ad Library TITLES only (connector) and never ran competitor_sweep.py, although the rule and script existed; Soumil caught it ("the most important step"). The sweep is the LEAD's job (the agents are barred from Apify), so nobody ran it. Fixed: SKILL.md now has a HARD GATE and a Stage 2 exit checklist (15+ brands, 250+ ads, sheets viewed, counted with scripts/creative_code.py, 60-ad audit by eye) and Gate 1 may not be presented without it; competitor_sweep.py downloads in parallel. First thing to say at the end of any Stage 2: the exit checklist with ticks and crosses, crosses first. See [[project-daigo-pilot-oct2026]] and [[reference-ad-library-browser]].
