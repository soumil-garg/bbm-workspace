# Data collection playbook (Stages 1 to 2, plus Stage 3 lessons in section 8), v2.1, 2026-10-09

Proven end to end on Daigo (instant chaas premix, India, 2026-10-09). It replaces the Chrome-on-Amazon and Arctic Shift routes in `research-playbook.md` sections 2 and 3, which stay only as fallbacks. The scripts are config driven: copy the example config from `references/examples/`, change the word lists, run `--dry-run`, then run for real. The dry runs reproduce the Daigo plans exactly (Reddit phase 2: 447 threads, 8,363 comments, 31 runs, $4.72).

## 0. Rules before any pull

1. **Name the account that spends: Apify Starter** ($19 a month, includes $19 of usage; cycle runs 8th to 7th). Run `python scripts/apify_status.py` first (read-only, free). The monthly usage limit equals the credit ($19) and Soumil said not to raise it (2026-10-09), so every pull must fit in the room left. Unused credit is lost at the end of the cycle: do not hoard it, do not spend it for its own sake.
2. **A yes per source, per brand.** Reddit, Amazon, Instagram and Flipkart are public data but terms-adverse. Ask once per brand and log the answer (Daigo: Reddit yes, Amazon yes instead of Flipkart, Instagram held, Flipkart dropped). Soumil's own logins are never used.
3. **Per-run caps.** Every run is started with `maxTotalChargeUsd` (the scripts do it). Budget with items x list price. The cost on the run object lags about a minute after the run ends, so it reads low at first (a $0.225 run showed $0.042). Re-read `apify_status.py` before a big pull. The `apify/google-search-scraper` refuses a cap under $0.50; that cap is a ceiling, not the spend.
4. **One cheap test before the pull.** A bake-off of 4 actors on one tiny query cost $0.44 and saved the run: one actor returned off-topic r/technology posts and billed for them.
5. **Public text only.** Strip names, handles, emails and URLs before text goes to Jev or Luna. Paraphrase in client material; no raw Reddit comments or usernames in decks.
6. **DataForSEO is not bought** (Soumil, 2026-10-09). Buy it only when a brand's decision needs exact search volumes (a search-led category). List prices read 2026-10-09: SERP page $0.0006 queued, $0.0012 priority, $0.002 live; volumes $0.06 per 1,000 keywords; $50 minimum deposit. Apify Google costs: $0.0025 per page, about $0.06 per Trends chart.

## 1. What a complete Stage 1 to 2 pack holds (and how it is made)

| Piece | How | Output files | Daigo cost |
|---|---|---|---|
| Meta account refresh | agent, official Meta connector only, read-only | campaigns.csv, daily_account.csv, ads_90d.csv, breakdowns.csv, impact_check.md, verification_checks.csv, scripts | $0 |
| Competitor map + ASIN list | agent (7-step checklist, Ad Library through the connector) | competitors.md, ad_library_findings.md, ad_library_rows.csv, asin_list.csv, ig_handles.csv, substitutes.md, gaps.md | $0 |
| Brand layer | agent (live site, on-site reviews, price ladder) | brand_layer.md, price_ladder.csv, public_reviews.json, customer_voice.md, competitor_sites.md | $0 |
| Claims audit (food, health, finance) | agent | claims_rules.md, claim_by_claim.md, claim_table.csv, festive_and_vrat.md, questions_for_brand.md, sources.csv | $0 |
| Open forums | agent | forum_digest.md, reddit_leads.md, pains_desires.md, questions_asked.md, words_people_use.md, substitutes_mentioned.md | $0 |
| Google | `scripts/google_pull.py` | autosuggest_summary.md, apify_serp.json, apify_trends_*.json | about $0.35 |
| Reddit | `scripts/reddit_pull.py` | p1_posts_all.json, p2_comments_all.json, p2b_comments_all.json, p1_comment_mentions.json | about $11 |
| Amazon.in | `scripts/amazon_pull.py` | amazon_reviews_all.json, amazon_summaries.json | about $1 |

Daigo yield: 3,416 Reddit threads found (about 630 mention the category words in Indian subs), 8,911 Reddit comments pulled, 748 Amazon reviews from 67 of 105 listings (56% critical), 2,500+ autosuggest completions, 153 People Also Ask questions, 344 open-forum texts. Total Apify spend about $12.6 of $19.

## 2. The five research agents (run them in parallel, first)

Brief template: `references/agent-brief-template.md` (copy it to `C:\cca\<brand>\research\_AGENT_BRIEF.md`, fill the client section). One folder per agent. Hard rules in the brief: research only (no spend, no Apify, no Chrome, no sign-ups), tag every finding Confirmed / Likely / Hypothesis with a source, digest of 5 to 10 lines at the top of each main file, final message at most 700 words (the harness refuses a REPORT.md from a subagent), no em dashes or asterisks in files.

**Agents stall.** On 2026-10-09 three of five stopped with "no progress for 600s" after 20 to 60 minutes and 0.5 to 0.75M tokens each; one had written nothing. Recover with SendMessage to the agent id (it resumes with its context), say "write your files now, then finish", and put in the brief: write each file as soon as its section is done. Check the folders (`ls`) when a stall notice arrives.

Known walls, so agents do not burn calls on them:
- **Competitors:** Ad Library through the official connector gives titles only (no body, format or landing page); allow about 40 calls. **Then open the top 5 to 8 advertisers in the Ad Library WEB UI with the built-in browser (logged out, free): it returns the full body copy, headline, offers and the creatives, which the connector does not (recipe: memory note reference-ad-library-browser; Daigo 2026-10-09 found the title pass had missed home and nostalgia hooks in Pod and Cup-Ji body copy).** Amazon.in returns 503 to fetch tools; Zepto and Instamart pages are script-only or 403. The ASIN list comes from amazon.in-restricted web searches and needs columns `asin,title,brand,group,url,rating,ratings_count,source`.
- **Forums:** Reddit is unreadable by fetch tools. Arctic Shift returned 422 "Timeout" for hours, PullPush 429, the redlib mirrors 410 or 429, Brave Search result pages rate-limit after about 9 calls, Quora pages are 403 (question titles show in WebSearch with allowed_domains). Tripadvisor, Lybrate, Practo, Careers360 and MouthShut give readable text.
- **Claims:** the ASCI complaints database answers its own public search endpoints (about 70 paced requests, no key). FSSAI's amendments page is script-rendered; consumeraffairs.nic.in refused. Output verdicts per claim: DO NOT SAY, CHANGE TO, CAN SAY WITH PROOF, CAN SAY AS IS, with the rule cited. Daigo audit: 42 claims, 24 DO NOT SAY (the whole health layer), plus site-wide exposure (blog posts, comparison tables, footer words). Feed the table into Stage 4b.
- **Brand layer:** Shopify `/products.json` gives live prices; the review widget (Judge.me) returns JSON; check badges that are hard-coded text against the widget count. Amazon blocked.
- **Meta refresh:** official connector only, read-only. Verification checks that must pass before any number is quoted: the account total equals the sum of campaigns on every day; the ads sum to the account; a re-pull matches; split date ranges and weekly blocks add up. Save the CSVs and the scripts that rebuild them.

## 3. Google (`scripts/google_pull.py`)

- `autosuggest`: free, 500 queries in about 4 minutes, no volumes. English and Hinglish seeds in three groups (problem, category, brand) plus modifiers and a to-z pass.
- `serp`: one results page per query. Returns People Also Ask (153 questions from 40 queries), related searches, organic results. Queries in Hinglish return Hindi PAA.
- `trends`: one comparison chart of up to 5 terms, 5 years, India. Gives the month-of-year profile, the state split, related and rising queries. **Unreliable:** 1 of 4 runs finished (130 s), the others timed out at 130 to 290 s and each failed run still bills about $0.09. Run it once, with a 290 s timeout, and do not retry in a loop; if a second chart matters, do it by hand in the browser (free) or pay DataForSEO ($0.0027 a task).
- Reading Trends: values are relative and sampled. A small term next to a big one shows 0 or "<1" (too small to register), not zero searches. English words can mean something else: "buttermilk powder" returns US baking results even with India set.
- `trends_report`: local read of the saved charts.

## 4. Reddit (`scripts/reddit_pull.py`)

Why Apify: the free archives are unreliable and Reddit blocks every fetch tool. Actors and Starter prices read 2026-10-09:

| Job | Actor | Price | Note |
|---|---|---|---|
| Find posts (phase 1) | fatihtahta/reddit-scraper-search-fast | $0.00139 per item (posts and comments alike) | dateFrom/dateTo, strictSearch, strictTokenFilter, subredditName + subredditKeywords; 30 s per run |
| Comments (phase 2) | automation-lab/reddit-scraper | $0.003 start, $0.001 post, $0.0005 comment | takes post URLs; about 1 item per second, so run 8 in parallel |
| Brand mentions in comments | harshmaur/reddit-scraper | $0.02 start, $0.0018 per result | `searchComments` finds comments across Reddit; good for brand names, noisy for generic words |
| Rejected | logiover/reddit-historical-archive-scraper | $0.00135 per item | returned 40 off-topic r/technology posts and billed for them |

Method that worked:
1. **Strict matching.** The bare word "chaas" returned memes and names ("Chaa mud gyi", "Chaa Thai Pea"): only 3 of 15 posts were about the drink. Use `strictSearch` and `strictTokenFilter`, multi-word queries, and word-boundary regexes for relevance (a plain `lassi` matches "classic"; this inflated the first count from about 630 to 907).
2. **English words only count in India-related subreddits** (buttermilk is also a US baking word). Indic words (chaas, chaach, mattha, jaljeera) count anywhere.
3. **Newest first plus caps cut older years.** Phase 1 gave 2026: 621 of 907 loosely matched posts. The top-up phase runs date windows for older years; it added only 103 posts and 874 comments for $1.0, so history before 2025 was thin for this category.
4. **Tiers for phase 2:** T1 category word in the title, T2 word in the body inside an India subreddit, T3 use-case or brand threads (train, hostel, summer drinks, digestion, protein, Amul, Trustified) with enough comments. The script lowers the per-thread comment caps step by step until the plan fits the budget.
5. **Daigo yield:** phase 1 cost about $5.2 (44 runs, 3,416 posts; the budget was $4.5 and parallel runs overshot), phase 2 about $4.6 (31 runs, 8,037 comments), top-up about $1.0.
6. Raw files hold usernames; keep them in the private research folder and strip before counting.

## 5. Amazon.in (`scripts/amazon_pull.py`)

- **jaybird/amazon-reviews-scraper** ($0.00092 per item, domain `amazon.in`): a summary row per listing (average, rating count, **star histogram in percent**) plus the product page's top reviews (about 4 per listing, up to about 13). 105 listings gave 475 items for about $0.44.
- **axesso_data/amazon-reviews-scraper** ($0.0009 per review, `domainCode: in`): review pages with `sortBy`, `maxPages` and `filterByStar` (one_star, two_star, three_star). **It gets past the 13-review wall:** one listing gave 55 unique reviews (21 of them 1-star) from 3 pages x 3 filters. Used for the critical reviews of the big listings and for small listings in full. Empty pages come back as `NO_REVIEWS_PENALTY_n` (ignored).
- Order: `depth` test on the biggest listing (passes at 25+ unique reviews) -> `public` -> `deep` (top 8 listings, 1 to 3 star) -> `compile` -> `ext` (every listing where Amazon shows more ratings than we hold). `all` runs the lot.
- **Ratings are not reviews.** Many ratings are star-only and reviews can be pooled across flavours. Daigo's main listing: 2.9 stars from 44 ratings (48% rated 1 or 2 stars), but the 28 written reviews held are 21 five-star and 7 critical, more five-star reviews than the histogram has five-star ratings. Quote the histogram for the rating mix and the text for the themes, and say they do not line up.
- Dead ends: `jdtpnjtp/amazon-reviews` has no India; DataForSEO's Amazon reviews endpoint is documented as down; Chrome with a logged-in profile risks the account (Amazon cuts flagged accounts to 8 reviews).
- Daigo yield: 748 reviews, 578 with 20+ characters of text, 419 critical (56%), 67 of 105 listings, about $1.0. The category is thin on Amazon (the whole instant chaas group holds 100 ratings), so the 1,500-review target needs Reddit comments and forums as well; report the pool as pooled.

## 6. After the pulls (Stage 2 compile and counting)

1. **Pools by source, never mixed.** `references/examples/build_pool_daigo.py` shows the pattern: Amazon reviews (title + body, stars kept), Reddit comments with the thread title in front as "title || comment" (so a reply like "it is too thick" keeps its subject), Reddit posts, open-forum texts. Drop deleted or removed texts and texts under 25 characters, dedupe by id, leave brand-hosted reviews out of independent counts, drop baking threads (the "buttermilk powder" comment search returned US baking), keep Reddit comments from body-match (T2) threads only when the comment itself names the drink. No username enters a pool. Daigo pools: Amazon 713 texts, Reddit core 4,313, forums 259.
2. **Theme questions per source** (rules in `references/theme-question-rules.md`; worked sets `references/examples/themes_amazon_daigo.json`, 20 questions, and `themes_reddit_daigo.json`, 17 questions). Write them after reading 20 to 40 samples per pool (print them; do not guess). Explicit statements only, "Answer no if ..." inside the text. Reddit sets start with a relevance question (`on_topic_drink`) and every question says the text is "thread title || comment" and to judge the comment.
3. **Count:** `scripts/theme_counter.py --reviews pool.json --themes themes.json --out OUT --audit 100` (Jev counts everything, Luna reads everything as second reader; flagged = Jev between 0.25 and 0.75, models disagree, or Luna refused). Cost on Daigo: about $2 for both pools (Jev about $0.04 per 1,000 texts, Luna about $0.35). Default is 4 workers per model, which is slow on long prompts (the Reddit run managed about 85 texts a minute and would have taken 85 minutes); use `--workers 10` and Jev and Luna run at the same time (the Reddit pool then finished in 15 minutes). Results are cached per text and question set, so a stopped run resumes without paying twice. Start it in the background.
4. **Blind audit, three labellers who never see model output:** `scripts/audit_make.py` replicates the counter's sample so labelling can start while it runs; `scripts/audit_label_mini.py` (gpt-5-mini, about $0.12 per 100 texts); a fresh Claude sub-agent told to read only the audit folder; Claude main last. For a pool that is mostly off-topic (Reddit) draw the sample from the texts the counter's relevance question calls on-topic (pass the subset ids), or the audit has too few positives. `scripts/audit_score.py` scores the counter: CLEARED = at least 5 key positives, precision at least 0.75, share error within 5 points; under 5 key positives = UNTESTED. **For themes that are not cleared or untested, quote the audit's own key share** (`scripts/audit_key_shares.py`: "54 of 100 random on-topic texts, 95% interval 44 to 63"); it needs no model and is honest about width. Daigo results: Amazon 12 of 20 themes cleared (Jev macro-F1 0.93, 97.7% unanimous labels), Reddit 3 of 17 cleared (macro-F1 0.80); the Reddit audit sample came from the on-topic subset, where the on-topic filter was 96% precise.
5. **Tables:** `scripts/counts_report.py --pool ... --counter-out ... --audit-results ... --title ... [--base-theme on_topic_drink]` writes the cleared-themes table with Wilson intervals, the raw counts of the rest, and verbatim samples cut to 15 words. Slice by product group (chaas family vs other drinks) and mark slices as not separately audited.
6. **Write the Stage 2 section** in the vault note (template: `Projects/daigo-creative-research-oct2026.md`): digest, coverage and limits table, counted pains (only cleared themes get a share with its Wilson interval; list the untested), words people use, substitutes, awareness sizing, competitor page, claims and safety, strategic read marked as hypotheses, evidence quality.

## 7. Pitfalls (each one cost time or money on Daigo)

| Pitfall | What happened | Do instead |
|---|---|---|
| Free Reddit archives | Arctic Shift 422 for hours on 7 and 9 Oct, PullPush 429 | Apify actors |
| Loose word match | "lassi" inside "classic", "chaas" as a name | word boundaries, strict filters, India-sub rule |
| Trusting run cost | showed $0.042 for a $0.225 run | items x price, re-read usage |
| Cap under $0.50 on google-search-scraper | run refused | set $0.50 |
| Trends retries | 3 of 4 runs timed out, each billed | one run, 290 s timeout |
| Parallel runs vs budget | phase 1 est $5.2 vs $4.5 budget | the guard checks before launching, so keep the budget below the true ceiling |
| Wrapping stdout twice in Python | closes the stream and crashes | import `apify_lib` once (it sets UTF-8) |
| Heredoc Python with backslashes | `\\` collapsed, a CR in a path | write scripts with the Write tool or use forward slashes |
| Agents write files only at the end | a stalled agent left an empty folder | write as you go |
| Counter at 4 workers | Reddit run would have taken 85 minutes | `--workers 10`, cache makes restarts free |
| Audit sample drawn from an off-topic-heavy pool | too few positives per theme | draw it from the on-topic subset (`audit_make.py` with subset ids) |
| Quoting a share for a theme the audit did not clear | would mislead the copy | quote the audit key share with its interval, or say untested |

## 8. Stage 3 lessons from Daigo (2026-10-09)
- **Segment axis:** "the first worry that stops a purchase" gave clean, sized segments (taste, trust, format, value) from the counts; the cold viewer who has never seen the product type is a state, not a segment, so reach them with explain-format concepts inside the primary segment.
- **The claims audit is a Stage 3 input, not only a Stage 4 gate:** write the voice lines first (SKILL.md Stage 4a), use the audit's safe-lines list only as a filter that fixes wording, and map every live ad headline to pass / reword / pause at Gate 1 (Daigo: 5 of 16 live statics carried a DO NOT SAY phrase, 6 needed rewording). Pausing live ads is Soumil's call.
- **Contradictions go to Gate 1:** the July brief (cast men for cold) against the October refresh (women convert cheaper); test both.
- **Do not invent the SAID half of the ICP card.** If the client onboarding call has not happened, say so and list the 12 live questions (`Resources/Ad Inspiration/icp-onboarding-questionnaire.md`) plus the proof documents the claims audit asks for.
- **Do not repeat numbers from older vault notes as facts** (the Daigo master note had figures later found wrong); re-pull and verify.
- **Persona names in the overlap test are illustrative**; label them so.
- **Time and cost of the whole Stage 1 to 3 run on Daigo:** about 8 hours elapsed including agent stalls, Apify $12.6, OpenAI and Jev about $2.3, five research agents (0.5 to 0.75M tokens each).
