---
name: feedback-ground-spend-caps
description: Never propose a spend cap (like $10) without saying which account it would come from; Soumil challenged an ungrounded $10 on 2026-10-07
metadata:
  node_type: memory
  type: feedback
  originSessionId: 891b74f0-8beb-4d09-938f-31e9aa61b3c2
  modified: 2026-10-07T13:31:04.645Z
---

When I suggest a budget or cap, name the exact account it would be charged to and what real prices apply. Soumil asked "where is this $10 coming from? which tools are you using?" because I had floated a $10 ceiling with no source behind it.

**Why:** the only things on this machine that can spend money are the OpenAI key (his billing), the TypeSafe/Jev key (free credit) and the Apify token (free plan, hard cap $5 a month, about $1 left until 6 Nov 2026). I have no card and no other way to pay. A made-up number reads as if I could spend it and erodes trust in my other numbers.

**How to apply:** before any "cap", check the real balances or limits first (Apify via its API, OpenAI cost via the ledger in C:\cca\_ledger), quote real per-unit prices, and give the realistic total. Say plainly when a cost is zero (free sources, logged-in browser). Counting 1,500 reviews is about $0.60 total; the first real bills at scale are a paid review-fetching service and image generation. Related: [[reference_apify]], [[reference-jev-typesafe]], [[feedback_tone]].
