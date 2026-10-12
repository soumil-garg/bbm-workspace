---
name: reference-ad-library-browser
description: "How to read competitor ads in full (body copy plus creatives) in the Meta Ad Library web UI with the built-in browser, logged out; the connector returns titles only"
metadata:
  node_type: memory
  type: reference
  originSessionId: b3607133-6288-42df-85dd-d0d6d53e5a58
  modified: 2026-10-09T10:32:22.896Z
---

Verified 2026-10-09 on Daigo's category. The official connector `ads_library_search` returns only link titles, dates and page IDs (no body text, no creative). The Ad Library web UI shows both, with no login, in the built-in browser (Claude_Browser tools).

**Steps.** Navigate to `https://www.facebook.com/ads/library/?id=<ad id>`; it redirects to that advertiser's page view (all of its active ads, URL has `view_all_page_id`) with the ad open in a "Link to ad" modal. Wait 10 to 15 s (the first screenshot is often blank). `get_page_text` with max_chars 9000 to 30000 returns every listed ad's full body copy, headline, description, start date, platforms and "Low impression count, Impressions under 100" labels. For the creatives: `resize_window` to 1280x900 and reload (the layout breaks otherwise), then run JS that takes every `img` with naturalWidth above 300, walks up to the ancestor that contains exactly one "Library ID:", and overlays a fixed full-screen contact sheet of those images with their IDs; `screenshot` then reads about 300 px per ad. Nothing is downloaded. Reset the viewport with preset "desktop" afterwards.

**Limits.** Page IDs come from the connector rows (ad_library_rows.csv) or from the redirect URL. Video ads show only text or a poster. A creator or partner ad opens on the creator's page, which can say "No ads match". Each page lists the first 11 to 25 ads before "See more". Run length is still only a survival proxy, no spend.

**Why it matters.** The title-only pass said nobody used home or nostalgia hooks; the body copy showed Pod ("The drink your naani made") and Cup-Ji ("ghar-wali chai") both do. Always do this for the top 5 to 8 advertisers after the connector sweep. Notes: C:/cca/daigo/research/competitors/ad_creatives_browser_9oct.md; see [[project-daigo-pilot-oct2026]].
