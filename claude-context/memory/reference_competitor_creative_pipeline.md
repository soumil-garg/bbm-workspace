---
name: reference-competitor-creative-pipeline
description: "How to study 250+ competitor creatives and find the pattern: Apify sweep, numbered sheets, picture coding with audit, cluster sheets; costs, failures and the 32% to 75% audit lesson (Daigo 2026-10-09)"
metadata:
  type: reference
---

Run by the LEAD (agents may not use Apify). Folder per brand, e.g. C:/cca/daigo/competitors (config.json, brand_*.json, img/, sheets/, index.json, coded.json, pattern_counts.md, audit/).

1. `competitor_sweep.py fetch config.json` then `build config.json` (Apify curious_coder Ad Library actor, about $0.015 a brand; parallel resized downloads since 2026-10-09; the first sequential run with 2 MB originals crawled). 24 brands gave 401 ads, 257 with images. Use page_id when known; a name search keeps only ads whose page name contains the tokens (Rage Coffee kept 3 of 22), so set page IDs for big brands.
2. `creative_code.py code --index index.json --out coded.json --about "..."` (gpt-5-mini vision, about $0.35 per 257 ads; resumes). ALWAYS run `audit` (60 random ads, numbered sheets), label them by eye BEFORE opening audit_key.json, then compare. Daigo: the first prompt agreed 32% (83 of 138 statics called "native mock"); a `seen` free-text description first, plus renaming native_mock to fake_screen, gave 68 to 75% on 11 formats, 83% on 6 coarse groups, hooks 66 to 78%. gpt-5 scored the same on format at about 6 times the cost. Quote coarse formats, hooks indicative, devices checked on sheets.
3. `count --exclude "Brand,Brand" --dedupe` (drop restaurants and off-category brands, merge copies) then `sheet --field devices|format|hook --value a,b --min-age 60 --kind static` for numbered cluster sheets; view them yourself; send them to Soumil with SendUserFile (he wants to SEE the creatives).
4. Read: survivors (60d+) by brand (one brand can dominate: Sleepy Owl was 20 of 24 long-running statics), new tests (under 30d), offers, devices, own live ads vs the set, white space. Write the note in the vault (Projects/daigo-competitor-creatives-oct2026.md is the model).

Pitfalls: Meta Ad Library web UI (built-in browser) also shows full copy and creatives ([[reference-ad-library-browser]]) but the sweep is faster for 250+. Windows cp1252 console breaks on non-breaking hyphens when printing model text: use encoding utf-8. Skill hard gate: [[feedback-research-depth-minimums]] (file feedback_research_depth.md). See [[project-daigo-pilot-oct2026]].
