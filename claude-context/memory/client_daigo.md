---
name: client-daigo
description: "Daigo client — full context, ad account audit, campaign structure, creative performance, and flags. DEFAULT SESSION for Daigo work."
metadata: 
  node_type: memory
  type: project
  originSessionId: d57637df-d556-48c7-b786-c87fcc7ba533
---

# Daigo — Complete Client Context

**Product:** Instant premix buttermilk / chaas beverages — Daigo Buttermilk + Jaljira Chaas. D2C, daigolife.com.
**Goal:** Direct sales (OUTCOME_SALES)
**This session is the default session for all Daigo work.**

## ⚠️ MANDATORY: Read this first
At the start of every Daigo session, ALWAYS read the master doc:
`C:\Users\soumi\Documents\Vault\Projects\daigo-master.md`

That doc is the live source of truth — campaigns, performance, GA data, open issues, creative context. After any session where new data is gathered or decisions are made, update Section 10 (Update Log) and the relevant sections of that doc.

---

## Account Details
- **Ad Account:** act_1274511830515107 (Daigo ADS)
- **Facebook Page:** 430041706864822
- **Pixel:** 1728163678550529
- **Currency:** INR
- **Account age:** ~485 days (~16 months, since ~Jan 2025)
- **Total lifetime spend:** ₹60,485.69
- **Account balance (as of Jun 4, 2026):** ₹459.20 ⚠️ CRITICALLY LOW

---

## Active Campaigns (as of Jun 2, 2026)

### Campaign 1: "New Sales Campaign actual (targeted) #1"
- **ID:** 120249554248000460
- **Budget:** ₹1,000/day (changed to ₹400/day on Jun 4, 2026 — verify if intentional)
- **Started:** May 2, 2026
- **Objective:** OUTCOME_SALES
- **Two adsets:**

  **Ad Set #1 (120249554248010460) — Traveler Interests:**
  - Interests: Adventure travel, Travel
  - Behaviors: Frequent Travelers, Frequent international travelers
  - Geo: Mumbai 50mi, Pune 25mi, Delhi, Gujarat, Karnataka
  - Advantage+ audience ON (geo expansion allowed)

  **Ad Set #2 (120249558064490460) — Away from Hometown:**
  - Interests: Airbnb, Resort, Hotels, Job
  - Life events: Away from hometown
  - Geo: Same as above
  - Advantage+ audience ON

- **5 ads in each adset** (Ad#1–Ad#5, same creatives duplicated across both)

---

### Campaign 2: "Sales Campaign (retargeted) #1"
- **ID:** 120249902833730460
- **Budget:** ₹804/day
- **Started:** May 9, 2026
- **Objective:** OUTCOME_SALES
- **One adset (120249902833830460):**
  - Custom audiences: Website Vis 180 + Video 10+ sec + Insta Engaged 365
  - Geo: All India
  - Advantage+ audience ON (age + gender expansion allowed)
- **5 ads** (Ad#1–Ad#5, same creatives as targeted campaign)

---

## Custom Audiences
| Audience | Type | Size |
|---|---|---|
| Insta Engaged - 365 | Instagram engagement (365 days) | 42,500–50,000 |
| Video at least 10 seconds | Video view 10s (multiple videos) | 78,900–92,800 |
| Website Vis 180 | Pixel - all website visitors 180d | ~20 ⚠️ DEAD |
| Purchase 180 | Pixel - purchasers 730d | ~20 ⚠️ DEAD |
| Website vis 180 - purchase 180 | Website visitors excl. purchasers | ~20 ⚠️ DEAD |

**Critical note:** Website pixel audiences are essentially empty (~20 people). The "retargeting" campaign is not retargeting website visitors — it's running on warm social engagement audiences (video views + Insta engaged). The pixel is firing poorly or site traffic is very low.

---

## Performance — May 2–Jun 2, 2026 (Ad Level)

### TARGETED CAMPAIGN — Ad Set #1 (Traveler Interests)
| Ad | Spend | Purchases | Revenue | ROAS | CPP | CTR |
|---|---|---|---|---|---|---|
| Ad#2 | ₹16,334 | 119 | ₹48,216 | **2.95x** ✅✅ | ₹137 | 4.8% |
| Ad#5 | ₹691 | 3 | ₹1,116 | **1.61x** | ₹230 | 6.1% |
| Ad#1 | ₹166 | 0 | — | ❌ | — | 3.5% |
| Ad#4 | ₹231 | 0 | — | ❌ | — | 2.2% |
| Ad#3 | ₹17 | 0 | — | ❌ (tiny) | — | 1.9% |

### TARGETED CAMPAIGN — Ad Set #2 (Away from Hometown)
| Ad | Spend | Purchases | Revenue | ROAS | CPP | CTR |
|---|---|---|---|---|---|---|
| Ad#2 | ₹12,035 | 90 | ₹33,732 | **2.80x** ✅ | ₹133 | 4.5% |
| Ad#5 | ₹1,365 | 8 | ₹4,142 | **3.03x** ✅ | ₹170 | 5.9% |
| Ad#3 | ₹154 | 0 | — | ❌ | — | 1.9% |
| Ad#4 | ₹70 | 0 | — | ❌ | — | 4.0% |
| Ad#1 | ₹85 | 0 | — | ❌ (tiny) | — | 4.5% |

### RETARGETING CAMPAIGN — Single Adset
| Ad | Spend | Purchases | Revenue | ROAS | CPP | CTR |
|---|---|---|---|---|---|---|
| Ad#2 | ₹17,454 | 117 | ₹41,346 | **2.37x** ✅ | ₹149 | 6.0% |
| Ad#5 | ₹1,600 | 7 | ₹2,511 | **1.57x** | ₹229 | 5.9% |
| Ad#1 | ₹58 | 2 | ₹808 | 13.9x (tiny) | ₹29 | 4.6% |
| Ad#4 | ₹279 | 1 | ₹279 | **1.0x** ❌ | ₹279 | 3.8% |
| Ad#3 | ₹62 | 0 | — | ❌ | — | 3.9% |

---

## TOTALS (May 2–Jun 2)
| Campaign | Spend | Purchases | Revenue | ROAS |
|---|---|---|---|---|
| Targeted | ~₹31,148 | ~220 | ~₹87,206 | **~2.80x** ✅ |
| Retargeting | ~₹19,453 | ~127 | ~₹44,944 | **~2.31x** |
| **COMBINED** | **~₹50,601** | **~347** | **~₹132,150** | **~2.61x** |

---

## Key Creative Insight
**Ad#2 (creative ID: 3362252507274361) is the dominant winner.** It runs in both campaigns and accounts for ~236 out of ~347 total purchases. Same creative has performed well across both the traveler interest audience AND the away-from-hometown audience. Whatever this video is — it works.

**Ad#5 (creative ID: 1539091887925839)** is a consistent second performer with decent ROAS across all 3 adsets.

Ads #1, #3, #4 are getting very little budget (algorithm correctly deprioritizing them). They have near-zero purchases.

---

## Flags / Issues

### 🔴 URGENT: Account Balance ₹529.23
At ₹1,804/day combined budget, this covers less than 8 hours. Campaigns will auto-pause immediately. Top up NOW.

### 🔴 Pixel / Website Audience Dead
Website Vis 180 audience has only ~20 people. Pixel isn't working properly or the site gets essentially no organic/direct traffic. The retargeting campaign is not actually retargeting website visitors — it's a warm engagement audience campaign mislabeled as retargeting.

### 🟡 Retargeting ROAS Lower Than Targeted
Retargeting at 2.31x vs Targeted at 2.80x. Counterintuitive — retargeting should convert better. Root cause: the retargeting audience (video viewers, Insta engaged) is not actually high-intent website abandoners. They're just warm awareness audiences.

### 🟡 Old "BLNKT" Campaigns in Account
Two paused campaigns from Oct 2025: "BLNKT-TrafficAd" (OUTCOME_TRAFFIC) and "BLNKT-Awareness-Ad" (OUTCOME_AWARENESS). Mumbai-only targeting. Likely a different brand/product that used this account before Daigo's current setup. Not impacting active campaigns.

### 🟡 Adset #2 Getting Less Budget Than It Deserves
Ad Set #2 (Away from hometown) is actually performing slightly better ROAS than Ad Set #1 on Ad#2 (2.80x vs 2.95x) and notably better on Ad#5 (3.03x vs 1.61x). The algorithm seems to be sending more budget to Ad Set #1 because Ad#2 there has higher absolute volume. Worth watching — could consolidate or rebalance.

---

## Audience Strategy (Indirect Targeting Logic)
- **Traveler interests**: Adventure/travel interest + frequent traveler behavior = people who actually travel. On the road with no desi drink options. Core ICP.
- **Away from hometown**: People living away from family — Airbnb, hotel, Job interests + life event. Also targets NRIs implicitly. Maps to the "missing ghar ki chaas" emotional angle.
- **Both geos**: Mumbai 50mi, Pune 25mi, Delhi, Gujarat, Karnataka — covers metros with highest D2C penetration AND Gujarat which is historically strong chaas culture market.

---

## Paused Campaigns (Historical)
- **"New Sales campaign"** — Feb 2025, OUTCOME_SALES, ran 8 days. Had international geo targeting (UK, US, AU + India). Likely early testing.
- **"Daigo Insta DM"** — Feb 2025, OUTCOME_ENGAGEMENT, conversations objective. Homemakers + EG-Travellers adsets. Mumbai/Ahmedabad/Surat. Instagram-only.

---

## Google Analytics
**Property:** "Daigo" (ID: a329101245p458627893) under account "Daigo Chaas"
**Access:** soumilgarg1111@gmail.com (NOT soumilgarg0888@gmail.com which has unrelated properties)
**Period audited:** May 5 – Jun 1, 2026 (28 days)

### Top-Line GA Numbers
| Metric | Value |
|---|---|
| Transactions | 332 |
| Purchase revenue | ₹1,26,593 |
| Average order value | ₹381 |
| Active users | 4,200 |
| New users | 4,200 (essentially all new — almost no returning) |
| Sessions | ~4,476 |
| Avg engagement time | 46s |

### Sessions by Channel
| Channel | Sessions |
|---|---|
| Paid Social (Meta) | 3,600 (80%) |
| Organic Social | 347 (8%) |
| Organic Search | 243 (5%) |
| Direct | 195 (4%) |
| Unassigned | 61 |
| Organic Shopping | 17 |
| Referral | 13 |

### Active Users by Country (last 7 days)
India 827, United States 39, Canada 8, UK 3, Australia 2, Germany 2 (28-day: India 3.9k, US 142, Canada 44, UK 19, UAE 11, AU 11, SG 8)

### Product Performance (May 5 – Jun 1)
| Product | Views | ATC | Purchased | Revenue | % Revenue |
|---|---|---|---|---|---|
| INSTANT Masala Chaas Premix - 10 Servings | 665 | 634 | 261 | ₹72,819 | 57% |
| INSTANT Jaljira Chaas Premix - 10 Servings | 149 | 71 | 38 | ₹10,602 | 8% |
| Combo Masala+Whisker - 10 Servings | 116 | 21 | 10 | ₹5,290 | 4% |
| Combo Masala+Jaljira+Whisker - 20 Servings | 91 | 37 | 21 | ₹15,729 | 12% |
| 3x Masala Combo - 30 Servings | 59 | 64 | 16 | ₹11,984 | 9% |
| 2x Masala Combo | 53 | 15 | 5 | ₹2,645 | 2% |
| Masala+Jaljira Combo - 20 Servings | 22 | 13 | 6 | ₹3,174 | 3% |
| **TOTAL (19 products)** | **1,249** | **892** | **365 items / 332 txns** | **₹1,26,685** | |

### Purchase Funnel (session-attributed)
| Step | Users | Rate vs previous | Drop |
|---|---|---|---|
| Session start | 4,300 | 100% | — |
| View product | 797 | 18.5% | **81.5% bounce before product page** |
| Add to cart | 110 | 13.8% | 86.2% of viewers don't ATC |
| Begin checkout | 82 | 74.1% | 25.9% abandon cart |
| Purchase | ~51* | 62.5% | 37.5% abandon checkout |

*Session-attributed only. Actual transactions = 332 (multi-session journeys not captured)

### GA Tracking Issues
1. **Checkout event tracking broken**: `add_shipping_info` and `add_payment_info` events not firing. Checkout journey shows 0% at steps 2-4. Only `begin_checkout` fires.
2. **81.5% bounce rate before product view**: Most paid social traffic is not reaching product pages — suggests landing page or navigation issue, or Advantage+ expanding to low-intent audiences.

### GA vs Meta Discrepancy
- Meta reports: 347 purchases, ₹1,32,150 revenue
- GA reports: 332 transactions, ₹1,26,593 revenue
- ~4% gap — normal due to ad blockers, cross-device, attribution windows

---

*Audited: 2026-06-02 | Next review: when balance topped up and after 7 more days of data*
