---
name: reference-scraping-tools-oct2026
description: "Researched buy list for scraping and data tools (Reddit, Google, Amazon/Flipkart/Nykaa, ads, comments) with verified prices as of 2026-10-07; read before buying or building any scraper"
metadata:
  node_type: memory
  type: reference
  originSessionId: 891b74f0-8beb-4d09-938f-31e9aa61b3c2
  modified: 2026-10-09T05:14:28.089Z
---

Soumil asked (2026-10-07) for tools so he stops waiting on scraping; money is no object. Two research agents read vendor pages; full files: C:\cca\habbits\step2\tools\ (reddit_and_google.md, amazon_ads_social.md, options.csv, options2.csv). All prices are vendor-page figures read 2026-10-07, speed claims unverified until a bake-off is run.

**Update 2026-10-09 (Soumil's decisions, newest wins over the picks below):** Apify Starter was bought and its monthly usage limit stays at $19 (he said do not raise it). DataForSEO is NOT being bought now ("we aren't buying data for seo right now"); revisit when a brand needs exact search volumes (first search-led brand, e.g. Habbits oral care). Google bits for Daigo go through Apify instead (tested: SERP with People Also Ask $0.0025 per page, Trends about $0.06 per chart and slow), capped about $0.50. DataForSEO SERP prices re-read 9 Oct: $0.0006 queued, $0.0012 priority, $0.002 live per page. Reddit scraping approved 9 Oct (3 years). Amazon approved instead of Flipkart. Instagram held. Amazon depth: the axesso actor (axesso_data/amazon-reviews-scraper, $0.0009 per review, domainCode in) passed a depth test on 9 Oct: 55 unique reviews from one listing with a 1-star filter and 3 pages (21 one-star), so the 8 to 13 review wall is not absolute with it; results and costs in vault Projects/daigo-research-run-oct2026 and C:/cca/daigo/research/amazon.

**Primary picks:** (1) DataForSEO, $50 minimum, funds never expire, official MCP: autosuggest $0.60 per 1,000, SERP with People Also Ask and related $0.60-2.00 per 1,000, Google Ads India volumes $0.06-0.09 per 1,000 keywords, Trends $0.0027 per task, Google Maps reviews $0.075 per 1,000, YouTube comments $0.03 per 1,000. (2) Apify Starter $19 a month (NOT $39), Apify MCP: Reddit actors $1.49-2.00 per 1,000 results, Flipkart $1.99 per 1,000, Nykaa $2.00, Shopify review widgets (Judge.me, Loox, Yotpo) $0.80-1.20, Amazon public layer (jaybird, 8-15 reviews plus "Customers say" aspect counts) about $0.9, Meta ads curious_coder $0.75 per 1,000 ads. (3) Optional ScrapeCreators $47 per 25,000 credits that never expire, MCP: Instagram comments about $0.13 per 1,000 (agent's arithmetic), ad library fallback. Fallbacks: Bright Data (5,000 free records a month, Reddit $1.50 per 1,000, official MCP), Xpoz $20 a month (test first, history depth unclear), Serper.dev, YouTube Data API (free; search.list capped 100 calls a day).

**Corrections to my earlier advice:** DataForSEO's own docs call its Amazon Reviews endpoint "temporarily unavailable" (page modified 2025-03-07), so do NOT use it for Amazon reviews even though its sales pages quote $0.075 per 1,000 (I had recommended it; retracted). No vendor shows recent proof of deep amazon.in reviews unless fed your own logged-in cookie; logged-out gives 8 to 13 featured reviews per listing; Amazon limits flagged accounts to 8 reviews. Plan: build the 1,500 to 3,000 reviews from Amazon public layer + Flipkart (1,000-2,000 per product, negative-first) + Nykaa + brand-site widgets; deep Amazon optional (Unwrangle $99 a month with a throwaway login, or Apify cookie actors).

**Skip:** paid ad-spy tools (Foreplay $149-175 a month: no real spend or impression data for India), Reddit's official API (no comment keyword search, approval-gated), PullPush, Pushshift, Data365 (EUR 300 a month), SerpApi (3 to 40 times dearer), redditapis.com. TikTok is banned in India. Quora skip. Official Google Trends API still invite-only alpha.

**Risk notes:** Reddit v. SerpApi, Oxylabs and Perplexity survived dismissal on 31 Jul 2026; Google v. SerpApi refiled 10 Aug; Oxylabs MCP repo archived 16 Sep. Keep scraped output internal and paraphrase for clients. Arctic Shift (free Reddit archive) returned 422 (a timeout) and 429 for the lead and for the agent for hours on 7 Oct; retry later with ONE test call.

**Monthly cost at 5 to 10 brand runs (agents' arithmetic on list prices):** Reddit + Google stack $53-170; Amazon-public + Flipkart + Nykaa + ads + comments stack $70-220 (without deep Amazon); first month adds the $50 DataForSEO deposit. Questions Soumil must settle: Reddit history depth (60-90 days vs 2-3 years), comfort with vendors in a legal grey zone, monthly cap and queue vs live pricing, throwaway Amazon login yes or no (I advise no for now).

Related: [[reference_amazon_review_pull]], [[reference_apify]], [[feedback_ground_spend_caps]], [[reference_reddit_access]].
