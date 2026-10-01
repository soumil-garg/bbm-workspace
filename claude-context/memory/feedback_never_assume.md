---
name: Never Assume — Moiras Meta Ads
description: Explicit directive from Soumil to never assume anything about business, finances, ad accounts, or client work — always ask when unclear
type: feedback
originSessionId: 2babc3e2-8605-4a84-b808-f1408befa87f
---
Never assume anything when working on client campaigns, ad accounts, or anything business/finance-related. When in doubt about an ID, a parameter, a behavior, or an outcome — ask directly.

**Why:** Wrong assumptions on ad accounts (e.g., using wrong account ID act_1322736938617228 instead of act_968878865668383 for Moiras) caused a full batch of creative creation calls to fail. Soumil explicitly said: "You don't have to assume anything if you're not sure about it."

**How to apply:** Before making any write call (create, update, delete) on Meta or any other platform, confirm account IDs, form IDs, and any ambiguous parameters with the user if there's any uncertainty. Never infer from context alone when the cost of being wrong is a failed API batch.
