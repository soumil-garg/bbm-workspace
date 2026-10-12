---
name: reference_apify
description: "Apify account set up 2026-09-28 (free plan, $5/mo); token in Windows user env var APIFY_TOKEN; creator-outlier pipeline and its costs"
metadata:
  node_type: memory
  type: reference
  originSessionId: 4618a210-fb15-41b1-b925-84a04c1f5af7
  modified: 2026-10-07T13:31:00.109Z
---

Apify free plan ($5 credit/month, resets monthly). Token is stored as Windows **user** env var `APIFY_TOKEN`. Read it with PowerShell `[Environment]::GetEnvironmentVariable('APIFY_TOKEN','User')`. Never print it.

Free-tier prices seen 2026-09-28: search scraper $0.0027/result, reel scraper $0.0026/reel (+$0.001 per run start), transcript add-on $0.048/reel (skip it; transcribe locally with faster-whisper small.en, ffmpeg via scoop).

Lessons: Instagram keyword search only matches usernames, so seed with known creator names instead. **Check `paidPartnership` before trusting an outlier**: Dara Denney's 10M-view reel was paid by OpenAI.

First output: vault `Resources/US Ads Creators Research/` (outlier report + CSV of 470 reels). Related: [[project_marketing_personal_brand]]

6 Oct 2026 (Lotus research): two agents used the free credit, which fell from 5.00 to about 1.00 for the month (it resets monthly). Amazon reviews: actor jdtpnjtp/amazon-reviews at USD 0.0018 per review works for older mass-market listings but returns only about 20 per star level per listing, and nothing for several premium brands; web_wanderer returned 0 US text reviews. Duplicates are common (sibling listings share reviews, 38 percent of rows paid for were duplicates), so dedupe before budgeting. Check credit through the API before any run. 1,500 competitor reviews needs either more credit or an Amazon-logged-in browser.

7 Oct 2026 API check (GET /v2/users/me/limits and /users/me): plan FREE, cycle 6 Oct to 5 Nov, usage $4.00 of the $5 hard cap, so about $1.00 left until 6 Nov; it cannot overspend, and a paid plan (about $39 a month last known, check) is Soumil's decision. Credential-like user env vars on this machine: APIFY_TOKEN, OPENAI_API_KEY, TYPESAFE_API_KEY, DROPBOX_*, MIVA_*, SOUMIL_WA_TOKEN. Nothing else can spend money.
