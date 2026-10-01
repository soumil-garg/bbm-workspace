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
Search the category on amazon.in to get ASINs (brand + 8-12 competitors): fetch `/s?k=<term>` and parse `[data-component-type="s-search-result"]`.
```js
const g1=async(asin,f,sort)=>{const r=await fetch(`/product-reviews/${asin}/?filterByStar=${f}&sortBy=${sort}`);
 const d=new DOMParser().parseFromString(await r.text(),'text/html');
 return [...d.querySelectorAll('[data-hook="review"]')].map(x=>({s:(x.querySelector('[data-hook*="star-rating"]')?.textContent||'').slice(0,1),
  t:(x.querySelector('[data-hook="review-title"]')?.innerText||'').split('\n').pop().trim(),
  b:(x.querySelector('[data-hook="review-body"]')?.innerText||'').replace(/\s+/g,' ').trim()}))};
// for each ASIN: [['critical','helpful'],['critical','recent'],['positive','helpful'],['three_star','helpful']]
```
If the fetch redirects to `signin`, the profile is not logged in: switch browser (`select_browser`). Data leaves Chrome by POSTing to a small local Python HTTP server (127.0.0.1:8765, CORS headers) from a NON-chatgpt page; chatgpt.com cannot fetch localhost. Read the JSON, flatten to text, read all of it.
Also read the brand's own listing page (`get_page_text`): directions, ingredients, price tiers, rating breakdown, "bought in past month".

## 2b. Substitutes and workarounds (required, any brand)
People often do not know the category exists; they solve the problem with something else. Their reviews show the problem in their own words and what they would switch for.
1. List 4-8 substitutes: ask at intake, then widen with (a) Google/Amazon autosuggest for the PROBLEM in plain words ("how to stop strap slipping", "blouse neckline gaping fix"), (b) Reddit/Quora threads asking how to solve it, (c) what competitors' ads say they replace. Include the non-product workaround (skip the outfit, stitch it, adjust constantly).
2. For each purchasable substitute, pull 3-5 top listings on Amazon and read critical, 3-star and positive reviews with the same script as section 2 (Savvy example: safety pins, double-sided fashion tape, body/boob tape, sticky bra, blouse alterations).
3. Extract per substitute: why people use it (what it gets right), where it fails (verbatim), the words they use for the problem with no category term, what they say they wish existed, price they pay.
4. Write a substitutes table into the vault note: substitute | why people use it | why it fails (verbatim) | implication for the creative. Use it for: problem language in explain creatives, enemy angles, switching triggers, price anchors, and to size the problem (volume of substitute reviews and monthly purchases).
5. Substitute reviewers are closer to the cold audience than reviewers of direct competitors: they have the problem but may not know the category.

## 3. Reddit (blocked directly; use Arctic Shift)
`python scripts/reddit_research.py --out C:\cca\<brand>\research --subs A,B,C --terms t1,t2 --from 2023-01-01 --top 45`
Title search needs a date window (script splits into yearly windows). It writes `reddit_posts.json`, `reddit_threads.json`, `reddit.txt`. Filter relevant threads by keyword and read the top comments; weight by upvotes; dentists/experts are often top-voted. Good Indian subs: IndianSkincareAddicts, IndianBeautyTalks, TwoXIndia, AskIndia, delhi, bangalore, mumbai, IndianMaleGrooming, plus category subs. See memory reference_reddit_access.

## 4. Competitors
`ads_library_search` by brand/page for the top advertisers (including category-adjacent leaders); prefer ads live 30+ days. Note formats, offers, hooks. Chrome Ad Library pages are heavy; keep to a few advertisers. Build a "claims competitors own" list.

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
