# Research playbook (Stages 1 and 2)

Save raw data to `C:\cca\<brand>\research\`. Write findings into the vault note. Multi-source always.

## 1. Meta past data (MCP `mcp__9c1ec85d...`)
Account by month:
`get_insights(object_id="act_<id>", level="account", time_range="maximum", time_breakdown="month")`
Output is large and gets saved to a file. Parse (utf-8!):
```python
import json
d=json.loads(json.load(open(F,encoding='utf-8'))['result'])
for s in d['segmented_metrics']:
    m=s['metrics']; g=lambda k:next((x['value'] for x in m.get(k,[]) or [] if x['action_type']=='omni_purchase'),'0')
    sp=float(m.get('spend',0)); rv=float(g('action_values')); print(s['period'],round(sp),g('actions'),round(rv),round(rv/sp,2) if sp else '-')
```
Ad level per era: `get_insights(level="ad", time_range={"since":..,"until":..}, limit=200)`, rows under `d['data']`, sort by spend, print spend / purchases / ROAS / CTR / ad_id / ad_name.
Creatives: `bulk_get_ad_creatives(ad_ids=[...], account_id="act_<id>", fields="id,name,thumbnail_url,image_url,body,title,object_type,object_story_spec,asset_feed_spec{bodies,titles,descriptions}", limit=30)` (save file, parse `results[].creative`). Copy is in `body/title` or `object_story_spec.link_data|video_data`, or `asset_feed_spec`. Download `image_url` with urllib, contact-sheet them, view.
Audience: `get_insights(level="account", breakdown="age,gender", time_range=<best era>)` and again for now. Compare shares of spend and ROAS.
Rules: judge on purchases/ROAS, not CTR; note pauses/restarts; note formats saturation.
Shopify: `https://<site>/products.json?limit=250` for titles, variants, prices, compare-at, availability.

## 2. Amazon reviews (Claude in Chrome, profile logged into Amazon)
> **v2.1 (2026-10-09): this Chrome method is now the FALLBACK.** The primary route is `scripts/amazon_pull.py` (Apify, no login, no Chrome profile; see `data-collection-playbook.md` section 5). Use the Chrome route only if Apify is unavailable, and remember it risks the logged-in account (Amazon cuts flagged accounts to 8 reviews).
**Volume rule (Soumil, 2026-10-04): the old 25-reviews-per-product pull was too thin to see a pattern. Pull deep, and weight it to the NEGATIVE reviews, because the 1-star and 2-star reviews are where customers state their real concerns and objections.**
- Targets per brand run: at least 1,500 reviews in total, at least 60% of them 1-3 star. Deep tier: the client's own products plus the top 5 competitors (up to 5 pages for each of 1-star, 2-star and 3-star, 2 pages for 5-star, 1 page for 4-star, so up to about 170 reviews per product). Shallow tier: the remaining competitors and substitutes (1-star and 2-star pages 1-2, 3-star page 1, 5-star page 1).
- Take every critical review in full (title and body), not only the first lines. Competitor 1-star reviews are as valuable as the client's own: they are the unmet need we can answer.
- Stop paging a filter when a page returns no new reviews. If Amazon blocks deep paging (sign-in redirect, captcha, empty page after 10), record what you got and say so.
- Count, do not just read. Code each critical review into themes (taste, price, packaging, delivery, side effects, results not seen, fake or counterfeit, customer service, texture, smell, sizing, safety, "did not work", etc.) and put the count in the pains table as "n of N critical reviews". A theme with 40 mentions outranks a vivid quote that appears twice. Do the coding with a script plus a manual read; keep the verbatim quotes per theme.
Search the category on amazon.in to get ASINs (brand + 12-15 competitors, more when the market is crowded): fetch `/s?k=<term>` and parse `[data-component-type="s-search-result"]`.
```js
const g1=async(asin,star,sort,page)=>{const r=await fetch(`/product-reviews/${asin}/?filterByStar=${star}&sortBy=${sort}&pageNumber=${page}`);
 const d=new DOMParser().parseFromString(await r.text(),'text/html');
 return [...d.querySelectorAll('[data-hook="review"]')].map(x=>({s:(x.querySelector('[data-hook*="star-rating"]')?.textContent||'').slice(0,1),
  t:(x.querySelector('[data-hook="review-title"]')?.innerText||'').split('\n').pop().trim(),
  b:(x.querySelector('[data-hook="review-body"]')?.innerText||'').replace(/\s+/g,' ').trim()}))};
// per ASIN, deep tier: for star of ['one_star','two_star','three_star'] pages 1..5 (sort 'helpful', and again with 'recent' pages 1-2),
// ['five_star'] pages 1-2, ['four_star'] page 1. Dedupe by title+body. Stop a filter when a page is empty or all-duplicate.
// (filterByStar=critical and =positive also work for the shallow tier.)
```
**Amazon.in limits learned on Savvy (2026-10-05):** (1) `pageNumber` no longer pages review lists: page 2 and 3 return the same 10 reviews as page 1, so one query = 10 reviews at most. Get depth with `filterByKeyword=<word>` combined with `filterByStar=critical` (or one_star / positive) and both `sortBy=helpful` and `sortBy=recent`: about 45 category keywords per listing gave 60-150 unique critical reviews on listings with 100+ one-star reviews. Listings with few reviews are exhausted after the first pass. (2) Do NOT use `setTimeout` or `sleep` inside the in-page loop: Chrome throttles timers in background tabs (a 0.4 s sleep stretched to minutes). Chain `await fetch` only. (3) Do not run more than 2 loops at once in one tab: after about 1,500 fetches Amazon tarpitted the session (0.7 s became 17-42 s per request); stop and say so. (4) `stop` flags only act between listings; navigate the tab to kill a running loop. (5) Output containing URLs or query strings is masked by the tool: return only counts and pathnames. (6) Budget realistically: reaching 1,500 reviews needs more listings (30+), not more keywords on the same ones.
If the fetch redirects to `signin`, the profile is not logged in: switch browser (`select_browser`). Data leaves Chrome by POSTing to a small local Python HTTP server (127.0.0.1:8765, CORS headers) from a NON-chatgpt page; chatgpt.com cannot fetch localhost. Read the JSON, flatten to text, read all of it.
Also read the brand's own listing page (`get_page_text`): directions, ingredients, price tiers, rating breakdown, "bought in past month".

## 2b. Substitutes and workarounds (required, any brand)
People often do not know the category exists; they solve the problem with something else. Their reviews show the problem in their own words and what they would switch for.
1. List 4-8 substitutes: ask at intake, then widen with (a) Google/Amazon autosuggest for the PROBLEM in plain words ("how to stop strap slipping", "blouse neckline gaping fix"), (b) Reddit/Quora threads asking how to solve it, (c) what competitors' ads say they replace. Include the non-product workaround (skip the outfit, stitch it, adjust constantly).
2. For each purchasable substitute, pull 3-5 top listings on Amazon with the same deep, negative-weighted script and volume rules as section 2 (Savvy example: safety pins, double-sided fashion tape, body/boob tape, sticky bra, blouse alterations). Soumil, 2026-10-04: the substitutes' NEGATIVE reviews are a main insight source for the ads, so give each substitute at least 100 reviews, at least 60% of them 1-3 star, and count themes the same way (n of N critical reviews). A substitute with fewer than about 50 total reviews goes in the table as "thin data".
3. Extract per substitute: why people use it (what it gets right), where it fails (verbatim and counted), the words they use for the problem with no category term, what they say they wish existed, price they pay. Turn each counted failure into an ad angle candidate: "X fails because ..., we do ..." (enemy angle, comparison, problem-fix split), then check the claim can be backed before use.
4. Write a substitutes table into the vault note: substitute | why people use it | why it fails (verbatim) | implication for the creative. Use it for: problem language in explain creatives, enemy angles, switching triggers, price anchors, and to size the problem (volume of substitute reviews and monthly purchases).
5. Substitute reviewers are closer to the cold audience than reviewers of direct competitors: they have the problem but may not know the category.

## 3. Reddit (blocked directly; use Arctic Shift)
> **v2.1 (2026-10-09): Arctic Shift is now the FALLBACK.** It returned 422 "Timeout" for hours on 7 and 9 Oct. The primary route is `scripts/reddit_pull.py` (Apify, two phases, budget guarded; `data-collection-playbook.md` section 4).
**2026-10-05: Arctic Shift returned 429 and 422 ("Timeout. Maybe slow down a bit") on every request for about two hours, and the script exits quietly with no files. Test one call first (`get('posts/search', ...)` returns [] when it is failing); if it fails, log "Reddit unavailable today" in the vault note, do not loop, retry later.**
`python scripts/reddit_research.py --out C:\cca\<brand>\research --subs A,B,C --terms t1,t2 --from 2023-01-01 --top 45`
Title search needs a date window (script splits into yearly windows). It writes `reddit_posts.json`, `reddit_threads.json`, `reddit.txt`. Filter relevant threads by keyword and read the top comments; weight by upvotes; dentists/experts are often top-voted. Good Indian subs: IndianSkincareAddicts, IndianBeautyTalks, TwoXIndia, AskIndia, delhi, bangalore, mumbai, IndianMaleGrooming, plus category subs. See memory reference_reddit_access.

## 4. Competitors (no browser: Apify sweep, with images)
Script: `scripts/competitor_sweep.py` (fetch, build, report). It uses the Apify Facebook Ad Library scraper (about $0.04 per brand of 30 ads; token in env APIFY_TOKEN) and needs no Meta token and no browser. Proven 2026-10-04 on 15 brands, 867 ads, about $0.65. Write-up of that sweep: vault `Resources/Ad Inspiration/competitor-sweep-oct2026.md`.
1. **Pick brands (Soumil, 2026-10-04: at least 15, more in a crowded market).** Minimum 15 brands, 20-25 when the category is competitive: direct competitors (5-8), category leaders (3-5), adjacent or aspirational brands from other categories with the same buyer (3-5), plus 2-3 brands in the client's other markets if relevant. Find them from Amazon search results, Reddit mentions, the client's own list and `ads_library_search`. Put them in `config.json` with role, industry, country and `page_id` when known (page_id is more reliable than name search; if a brand returns 0 rows, find its page_id and re-run).
2. **Fetch:** up to 30 active ads per brand, sorted by total impressions. `python scripts/competitor_sweep.py fetch config.json`. Increase `per_brand` to 50-80 for big advertisers.
3. **Build:** `python scripts/competitor_sweep.py build config.json` downloads the images, splits every ad into genuine static, video and catalog (DCO and DPA can hide video, so it checks for video files rather than trusting display_format), and writes a numbered contact sheet per brand (up to 20 statics, longest-running first, plus up to 8 video thumbnails with orange badges).
4. **Look at every sheet.** View the images, do not rely on the copy text alone. Since v2.2 run `scripts/creative_code.py code` first (a vision model codes every picture into format, hook, offer, people, setting, text amount, palette, claims, idea and device for about $0.002 an ad), then `count`, then view the numbered cluster sheets (`sheet --field format --value fake_screen`) and read them yourself, and `audit` 60 ads by eye before quoting any count. **Lesson (Daigo, 2026-10-09):** the first coding prompt agreed with a by-eye audit on only 32% of 60 ads (it called 83 of 138 statics "native mock"); making the model describe the picture first (the `seen` field) lifted format agreement to 75% (83% when the 11 formats are merged into 6: product-led, text card, people or scene, fake screen, humour, other) and hook agreement to 66 to 78%, at about $0.002 an ad with gpt-5-mini (gpt-5 scored the same on format and cost about 6 times more). Quote formats at the coarse level, treat hooks as indicative, and never skip the audit. The older by-eye tagging in `tags.json` still works: bucket (1 Proof incl. authority, 2 Benefit headline, 3 Offer incl. seasonal and reason-why, 4 Native and atypical, 5 Product hero or lifestyle, 6 Explain or mechanism, 7 Compare or transform), offer, hook, format. Then `report` gives counts per bucket, per brand and the share running 60+ days.
5. **Read the patterns:** format mix (video vs static), the offer spine of the category, one-offer-many-concepts brands, long-running ads (60+ days) and what they share, what only the top brands do, what nobody does (a gap). Also record the longest-running video concepts, because statics in many categories are a minority.
6. **Limits to state in the note:** IN and US commercial ads have no impressions or spend in the Ad Library, so run length is only a survival proxy, not ROAS. The tags are made by eye. Do not claim a bucket "works" from this alone.
7. **Output:** one page of patterns per industry (what to copy, what to avoid, the gap), the numbered sheets, the claims competitors own, and a short list of 8-12 reference ads to feed the inspiration library. Put it into the vault note and use it to seed Stage 3.

## 5. Claims and safety
Web search the facts that shape what we can say (regulation, clinical studies, e.g. charcoal abrasiveness: ADA 2017 review insufficient evidence). Cite sources in the vault note.

## 6. YouTube / Quora
YouTube comment pages freeze the renderer; treat as optional. Quora logged-out is low signal.

## 7. Awareness sizing (required)
Amazon reviewers and Ad Library advertisers are buyers and sellers, not the cold audience, so a crowded category does not mean cold viewers know it. Estimate cold awareness of the category term: (a) search interest for the category term vs the problem phrase (Google autosuggest, Trends if available), (b) Reddit/Quora posts asking "what is X" or "does X exist", (c) how often substitutes are mentioned vs the category term in reviews, (d) how many competitor ads explain the category vs assume it. Write one line in the vault note: "category awareness: known / half-known / new, because ...". Never write "everyone knows X" without evidence.

## 8. Planned: Grok
Soumil plans to use Grok for research in future (noted 2026-09-30). Not set up. Until he says how (paste, API), do not assume; mention it when a brand's research has gaps.

## Output (vault note)
Past-data findings (numbers table, top ads, audience drift), pains table (insight, confidence, verbatim), words people use, substitutes table, awareness sizing line, competitor-owned claims, claims to verify, strategic read.
