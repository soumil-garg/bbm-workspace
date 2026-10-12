---
name: feedback-tracking-audit-first
description: "STANDING RULE (2026-10-06): every new client onboarding starts with a tracking accuracy audit, Meta vs the store of record (Shopify, Miva, other); skill tracking-accuracy-audit, tool C:\cca\tools\tracking_audit, Part 0 of /onboard"
metadata:
  node_type: memory
  type: feedback
---

Before any Meta purchase, ROAS or CPA number from a new client is used for a decision, run the tracking accuracy audit: how the pixel is connected, then Meta (dataset stats, daily attributed purchases and value, server events, hosts) against the store's own orders. Verdict GREEN, AMBER or RED.

**Why:** 2026-10-06 Soumil, after Lotus Sculpture (Meta counted each sale about twice, sent under half the value, no server events since 27 Oct 2025, ROAS 11 looked great): "Every time we onboard any new client, we first have to check whether the setup is really accurate. Are Meta's numbers accurate with Shopify or the Miva store?"

**How to apply:**
- `/onboard` now has Part 0 for this. The skill is `tracking-accuracy-audit` (in ~/.claude/skills). The tool is `C:\cca\tools\tracking_audit\audit.py` (commands inventory, reconcile, insights2csv; regression tests regress_lotus.py and regress_healthy.py). The SOP is vault `Areas/tracking-accuracy-audit-sop`.
- Meta below the store is normal (attribution). Meta above the store, or about 2 Purchase events per order, is a defect. Neither Shopify nor Miva is accurate by default: Shopify's app usually gets the plumbing right but duplicates happen there too; Miva is manual and failed on Lotus.
- RED or AMBER: tell Soumil first, then report to the client as a finding with a short picture summary. Any live site or tracking change still needs the client's written OK (see [[client_lotus_sculpture]]).
- Read-only: never print tokens, never bypass a bot challenge, never press Save or Delete in a client admin, delete order exports at the end.
