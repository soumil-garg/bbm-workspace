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

## 3. Reddit (blocked directly; use Arctic Shift)
`python scripts/reddit_research.py --out C:\cca\<brand>\research --subs A,B,C --terms t1,t2 --from 2023-01-01 --top 45`
Title search needs a date window (script splits into yearly windows). It writes `reddit_posts.json`, `reddit_threads.json`, `reddit.txt`. Filter relevant threads by keyword and read the top comments; weight by upvotes; dentists/experts are often top-voted. Good Indian subs: IndianSkincareAddicts, IndianBeautyTalks, TwoXIndia, AskIndia, delhi, bangalore, mumbai, IndianMaleGrooming, plus category subs. See memory reference_reddit_access.

## 4. Competitors
`ads_library_search` by brand/page for the top advertisers (including category-adjacent leaders); prefer ads live 30+ days. Note formats, offers, hooks. Chrome Ad Library pages are heavy; keep to a few advertisers. Build a "claims competitors own" list.

## 5. Claims and safety
Web search the facts that shape what we can say (regulation, clinical studies, e.g. charcoal abrasiveness: ADA 2017 review insufficient evidence). Cite sources in the vault note.

## 6. YouTube / Quora
YouTube comment pages freeze the renderer; treat as optional. Quora logged-out is low signal.

## 7. Planned: Grok
Soumil plans to use Grok for research in future (noted 2026-09-30). Not set up. Until he says how (paste, API), do not assume; mention it when a brand's research has gaps.

## Output (vault note)
Past-data findings (numbers table, top ads, audience drift), pains table (insight, confidence, verbatim), words people use, competitor-owned claims, claims to verify, strategic read.
