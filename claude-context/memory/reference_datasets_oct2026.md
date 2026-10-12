---
name: reference-datasets-oct2026
description: "Verified shortlist of open datasets for the ad engine (Upworthy, AdControlCenter judge set, Sephora, Amazon Reviews 2023, Flipkart); Kaggle ads shelf is mostly synthetic; how to search Kaggle and Hugging Face without logins; nothing downloaded as of 2026-10-08"
metadata:
  node_type: memory
  type: reference
  originSessionId: 891b74f0-8beb-4d09-938f-31e9aa61b3c2
  modified: 2026-10-08T16:53:16.651Z
---

Scan of 2026-10-08, full table in vault Resources/Datasets for the ad engine - Kaggle and Hugging Face scan, 8 Oct 2026.md. Nothing was downloaded; downloads need Soumil's yes with names, source and size.

Worth using, in order: (1) Upworthy Research Archive on OSF (jd64p, CC BY 4.0, exploratory 14.3 MB + confirmatory 66.5 MB) for the pending LLM-judge backtest, about $3, which gates the persona and crowd tools ([[reference_jev_typesafe]], saved reels Claude + Jev persona tester and MiroFish); (2) AdControlCenter Human Expert vs LLM Judge, 500 real Facebook ads, CC BY 4.0, 377 KB on Hugging Face (human and LLM agree 26.8%, LLM says good 72% against 20%, single annotator, mostly developer tools, vendor is a competitor); (3) Sephora skincare reviews on Kaggle, 1M reviews, CC BY, 154 MB, needs his Kaggle login; (4) Amazon Reviews 2023 on Hugging Face (McAuley-Lab), the real oral-care source: Beauty_and_Personal_Care reviews 11.0 GB + meta 2.8 GB, Health_and_Household 11.4 GB + 2.5 GB, no license on the card, no search API, so it needs a streaming filter; the UCSD host fails TLS verification here and must not be bypassed; (5) Flipkart product reviews (205k) for a Hinglish slice. Kaggle has nothing for oral care or whitening, no real D2C Meta performance data, no real Hinglish product-review corpus. About 9 of 24 opened "ads" pages were synthetic; never trust Kaggle usability scores for realness.

How: Kaggle search results are readable without login in the built-in browser by running a page script that collects the anchors starting with /datasets/ plus the card text; Hugging Face https://huggingface.co/api/datasets?search=... works but resets connections now and then; OSF API lists the Upworthy files; the Hugging Face datasets-server search does not index Amazon Reviews 2023. Non-commercial licenses (Nykaa and Flipkart app reviews, CC BY-NC-SA) are internal tests only.

Round 2 (8 Oct, Soumil: only the AdControlCenter set is really helpful): other real ad data is partial: KAG Facebook conversion table (1,143 ads, no creative), ADS-16 (300 ads rated by 120 people, skip the personal photos), LAMBDA (2,205 YouTube ads with recall scores, MIT), PersuasionArena (same-account tweet pairs, likes), Criteo attribution and uplift, Taobao click logs (outcomes, no creative). None pairs creatives with results at scale, so the real route is to build it: own Meta accounts read-only (Habbits 198 ads already in hand; other accounts only with his say, see [[feedback_scope_salaj_only]]), Meta Ad Library India scrapes via Apify (about $0.6 to $0.75 per 1,000 ads), and his own good/fair/bad ratings.
