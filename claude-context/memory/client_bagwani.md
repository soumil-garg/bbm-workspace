---
name: client_bagwani
description: Bagwani by Neetu Khanna — Meta ad account ID, Shopify site facts, and the dead legacy WooCommerce URLs still sitting in old ads
metadata:
  type: project
---

Bagwani by Neetu Khanna (cold-pressed oils, skincare, ghee) — client of Big Bigger Media.

- Meta ad account: **1682300005612270** (business `bagwani_by_neetukhanna`, business_id 273374852240552). Lifetime spend ~₹17.3L across 69 campaigns; ASC Campaign alone is ~₹15.6L.
- Website **bagwani.co is Shopify** (products live at `/products/<handle>`, collections at `/collections/<handle>`). Product feed: `https://bagwani.co/products.json?limit=250`.
- **It was WooCommerce before ~March 2026.** Old ads point to `/product/<slug>/`, `/collection/<slug>/` and `/shop/?filter_cat=…`. **All of those now 404** — no 301 redirects were set up during the migration. Verified 2026-09-02: 40 of 109 exportable ads still carry dead links. Never copy a URL out of an old ad without checking it.
- Ads Manager MCP cannot return ad destination URLs (no `link_url`/`object_story_spec` field). To audit landing pages, use Ads Manager → More → Import and export ad configuration → Export → Export all (CSV, UTF-16, tab-delimited, `Link` column). Ads using multiple headlines/primary texts are silently excluded from that export.
- As of 2026-09-02 there is **no pain relief oil product page** on the site, though creative and a draft campaign (`Retargeting_CBO_02_Sep`) already exist.

Related: [[feedback_never_assume]], [[process_ad_creatives]]
