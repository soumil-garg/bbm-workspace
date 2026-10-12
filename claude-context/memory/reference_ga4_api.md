---
name: reference_ga4_api
description: "How GA4 API access works on this PC (scripts, login, token expiry) and the pitfalls that gave wrong numbers; read before pulling any GA4 data"
metadata:
  node_type: memory
  type: reference
  originSessionId: 4618a210-fb15-41b1-b925-84a04c1f5af7
  modified: 2026-10-06T06:33:44.304Z
---

GA4 is read through the Data and Admin APIs with Soumil's own OAuth Desktop client (Cloud project precise-equator-497708-d3), read-only scope analytics.readonly, signed in as soumilgarg1111@gmail.com. Files are in C:\cca\ga4: ga4.py (creds, props, report), ga4lib.py (`q(dims, mets, start, end, filt, order, limit, name)` returns a DataFrame and can save a CSV to out\), charts.py (14 charts), package.py (builds the Desktop md and html report plus the vault note). client_secret.json and token.json live there: never paste, upload or commit them. The app is in Testing status, so the refresh token can expire after 7 days: re-run login.py (login_hint above) or publish the app.

The same login sees other clients' properties (Daigo, Mera Health). Lotus is property 322925114 only; never mix them. Lotus analysis lives in [[lotus-sculpture-ga4-deep-dive-oct2026]] and [[client_lotus_sculpture]].

**Why:** the first Lotus pull gave wrong numbers several ways, and a wrong GA4 number in front of a client is costly.

**How to apply (pitfalls, all hit on 4 Oct 2026):**
- Advertiser metrics (advertiserAdCost, Clicks, Impressions) must be queried alone with date and sessionGoogleAdsCampaignName. Mixing them with session or transaction metrics inflated cost about 1000 times.
- GA4 estimates sessions, so the total, the sum of channel rows and the sum of country rows differ by 1 to 6 percent. Use the no-dimension total as the denominator and say "about" for shares. Orders and revenue match in every slice.
- The `year` dimension returns several rows, so sum them. A transactionId pull includes a "(not set)" row per day: filter it, and drop zero-revenue orders for order-size stats.
- landingPagePlusQueryString splits one page by query string and a 3,000-row cap loses the tail; use landingPage with limit 100000. In Miva, category and product pages share one URL pattern, so they cannot be split by URL (page_code is event-scoped).
- Admin API reads work with the same scope: property settings, key events, custom dimensions, Google Ads and BigQuery links.
- Check the unit before quoting: GA4 purchase revenue includes shipping and tax (7 percent above item revenue on Lotus).
- Added 6 Oct 2026 (Lotus, joined to Miva by transactionId): a monthly-dimension advertiser cost query returns about 30 times the true cost, so pull daily and sum; one add_to_cart event carried 1,999,999 units, so clip outliers; GA4 counts cancelled and returned orders as sales (118K and 39K on Lotus) and misses about 15 percent of real orders, so join to the store database before quoting revenue or regional trends (a "California decline" was only GA4 coverage falling from 95 to 84 percent); purchase fires on /INVC.html only since Jan 2026 and two key events built from every confirmation-page view inflate conversions.

**Re-login that worked (12 Oct 2026):** `python -u login.py` in the background from C:\cca\ga4, read the printed accounts.google.com URL from the log, open it with `Start-Process "C:\Program Files\Google\Chrome\Application\chrome.exe" <url>` (Soumil wanted Chrome, not the default Brave), he clicks Allow, log says "token saved". A plain background login did not open a tab on its own. Lotus has no payment-type dimension; Braintree orders in Miva are all from Apple devices, so Braintree = Apple Pay proxy (see ga4 deep dive note).
