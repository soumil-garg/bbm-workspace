---
name: reference_apify
description: Apify account set up 2026-09-28 (free plan, $5/mo); token in Windows user env var APIFY_TOKEN; creator-outlier pipeline and its costs
metadata:
  type: reference
---

Apify free plan ($5 credit/month, resets monthly). Token is stored as Windows **user** env var `APIFY_TOKEN`. Read it with PowerShell `[Environment]::GetEnvironmentVariable('APIFY_TOKEN','User')`. Never print it.

Free-tier prices seen 2026-09-28: search scraper $0.0027/result, reel scraper $0.0026/reel (+$0.001 per run start), transcript add-on $0.048/reel (skip it; transcribe locally with faster-whisper small.en, ffmpeg via scoop).

Lessons: Instagram keyword search only matches usernames, so seed with known creator names instead. **Check `paidPartnership` before trusting an outlier**: Dara Denney's 10M-view reel was paid by OpenAI.

First output: vault `Resources/US Ads Creators Research/` (outlier report + CSV of 470 reels). Related: [[project_marketing_personal_brand]]
