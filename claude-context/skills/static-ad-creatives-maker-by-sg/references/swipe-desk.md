# Swipe Desk: taste calibration from real ads (built 9 to 10 Oct 2026)

## What it is
A private Claude Artifact where Soumil reviews static ads from brands known for good statics in India and the US (never onboarded clients). One ad at a time, four stamps: Approve (A), Disapprove (D), Maybe (M), Others (O, a comment); optional reason chips (Copy, Layout, Colour, Idea, Photo, Type, Offer, Format) and a note. Endless since 10 Oct 2026: no daily limit, the queue refills on its own. It works on laptop and phone (same Claude login). Approved ads are filed by type and format into the inspiration library, and every decision feeds a taste profile that Stages 3 to 5 read before writing or designing anything.

Link: https://claude.ai/artifact/Uor2nfjf9ijzm9f9JYTzHp (private). Vault design note: `Projects/swipe-desk-oct2026.md`. Memory: project-swipe-desk.

## Why it exists
Soumil rejected all 17 Daigo round 1 creatives on 9 Oct ("text not going with the overall vibe, shit copywriting"). The engine had rules but not his taste at the level of a single ad. Reacting to real, proven statics takes him seconds an ad and teaches the engine which voice, layout and idea he likes.

## Files and commands (C:\cca\inspiration\swipe; copies in references/examples/swipe_desk/)
- `swipe_pool.py` builds the pool from the Apify Ad Library pulls (`pool\brand_*.json`): statics only, running 14 days or more, one per creative, near-duplicates dropped, onboarded brands excluded (`onboarded.json`), page-name clashes handled (PAGE_ONLY, DROP_BRANDS), up to 30 an ad per brand.
- `swipe.py code` vision-codes new pool ads (format, hook, offer, devices, headline, idea) with `creative_code.py` (gpt-5-mini, about $0.0015 an ad) and assigns one of 7 buckets.
- `swipe.py batch --n 200` builds the queue: undecided ads of the last queue first, then new ones (older ads preferred, at most 14 a brand), spaced so the same brand never repeats within 4 ads and the countries alternate.
- `swipe.py build` embeds the queue into `swipe_ui.tmpl.html` (WebP, 720 px; falls back to smaller images if the page nears 15 MB) and writes `swipe_page.html` (about 8 MB for 200 ads).
- `swipe.py process <file>` files approved ads into `Desktop\Ad Inspiration\Library\<bucket>\<format>\`, adds principle, template, funnel and awareness (vision), and rewrites `library.json`, `decisions_all.json`, vault `Resources/Ad Inspiration/Inspiration Library.md` and `Swipe Taste Profile.md`. `SWIPE_TEST=1` dry-runs into `test_out\`.
- `swipe.py last_at`, `refill --pulled <dir>`, `mark_published`: the daily job. `refill` processes the pulled decisions and rebuilds the page only when the live page has fewer than 100 undecided ads (prints PUBLISH: yes or no), topping up the pool first (`swipe_topup.py --if-unseen-below 150`) when fewer than 150 unseen ads remain.
- `swipe_topup.py` fetches the next 6 brands of `brands_backlog.json` through Apify (about $0.02 a brand) and refuses to run below $1.00 of room under the monthly usage limit.

## Daily job (scheduled task `swipe-desk-refill`, 06:30 local)
1. `swipe.py last_at` gives the newest processed decision time T.
2. ArtifactData `query` on `decisions` with where `at > T`, limit 1000, out_dir `db_pull\<date>` (follow `next_cursor`).
3. `swipe.py refill --pulled db_pull\<date>\decisions`.
4. On PUBLISH: yes copy `swipe_page.html` to the scratchpad and publish to the artifact URL (read the artifact first if the tool refuses), then `swipe.py mark_published`.
5. Log a dated line in the vault note. Never send messages.

## Rules
- Never raise the Apify usage limit; the feed may use only the room above the $1.00 reserve. Soumil sets any monthly feed allowance.
- Run length is only a survival proxy; India and US commercial ads show no spend. "Best brands" is a seed list (`fetch_config.json`, `brands_backlog.json`), editable.
- A decided ad is never shown again; undecided ads carry over. Run `process` before `batch`.
- Yield is about 3 to 5 usable statics per brand fetched (most ads are video or catalog); `media_type=image` in the Ad Library URL does not filter reliably through the actor.

## How the engine uses it
- Stage 3 and 4: read `Swipe Taste Profile.md` (approval rates by format, hook, bucket, country, brand; reasons ticked; his notes) and the approved library entries for the bucket before writing voice lines. Early read (14 swipes, 10 Oct): approvals are headline-led with something concrete for the reader (a question, a plain offer, a proof line); rejections are brand-name or vague mood lines.
- Stage 5: pick 1 or 2 approved library entries (bucket, funnel, awareness) as the layout and mood reference per concept.

## Construction analysis (2026-10-10)
- `construction_code.py` codes every decided ad with a vision model on layout, background, palette, product scale and treatment, person, headline size and case, type effects, offer device, lighting, finish, harmony between headline and picture, eye path and craft notes (about $0.003 an ad); `construction_code.py report` prints approved against disapproved. Findings and the recipes: vault `Resources/Ad Inspiration/Approved ads - how they are built.md`. Read it at Stage 5 before writing any prompt.
- `construction_selfcheck.py label image...` compares a finished creative with the approved patterns (run 10 Oct on Daigo rounds 3 and 4; about $0.003 a picture; writes `analysis\self_<label>.json`).
