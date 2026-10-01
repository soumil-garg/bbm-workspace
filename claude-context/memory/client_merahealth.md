# MeraHealth — Persistent Client Context
*Last updated: 2026-05-29*

## What is MeraHealth
Preventive health tracking app for Indian families. Core value prop: track health records, AI spots trends, get early alerts before small problems become expensive emergencies. Free beta — no paid monetization planned yet. Client is actively seeking investment funding.

**Website:** https://mera.health
**App:** Android on Google Play (`health.mera.android`). iOS listed as "Coming Soon" — NOT live yet.
**Platforms:** Web signup + Android app. No iOS.
**Contact:** hello@mera.health

## Our Relationship
Big Bigger Media runs Meta ads for MeraHealth. Lead generation account — a "lead" = user who completes full onboarding (OTP verified + onboarding screen completed). This fires the Meta pixel on the thank-you/completion state.

## Meta Ads Account
- **Account ID:** act_777565568463647
- **Custom conversion event ID:** 764834986708940 (pixel fires on OTP-verified + onboarding completion)
- **Pixel tracking:** Active on web signups. App signups (Play Store) are NOT tracked in Meta — attribution gap exists.

## PostHog Access
- **Project ID:** 351010
- **Connected via:** OAuth MCP server at https://mcp.posthog.com/mcp (not API key — the old phx_ key is dead)
- **Key events:** `ad_landing_viewed`, `phone_input_raw`, `otp_requested`, `otp_verified`, `onboarding_completed`, `record_uploaded`, `play_store_clicked`, `what_changed_viewed`
- **PostHog dashboard:** "MeraHealth — Acquisition Funnel" (dashboard ID: 1644231) — tracks landing → phone → OTP → onboarding funnel

## Current Campaign State (as of May 29, 2026)

### May 2026 Account Overview
- Total spend: ₹38,166
- Total leads (Meta): 296
- Blended CPL: ₹128.94
- Impressions: 10,08,259 | Reach: 6,51,564 | Video Views: 3,64,288
- Link Clicks: 2,124 | Landing Page Views: 1,595 | CTR: 0.39%

### Active Campaigns
| Campaign | Status | Budget | CPL | Notes |
|----------|--------|--------|-----|-------|
| C-1 (May 1) | ACTIVE | ₹800/day | ₹99.30 | Best performer. 211 leads. Pixel tracking ON. |
| C-3 (May 6) | ACTIVE | ₹100/day | N/A | Awareness only. 8.37L impressions, 3.09L video views at ₹2.79 CPM. Feeds retargeting pool. |
| C-5 (May 15) | ACTIVE | ₹400/day | ₹102.31 | 56 leads. New audiences: Indian Wellness & Fitness, Digital Transactors, Millennials. |
| C-6 (May 25) | PAUSED (Under Review) | ₹1,500/day | Not launched | Consolidated best audiences from C-1 + C-5. Ready to launch. |

### Paused Campaigns
- **MH Actual #1:** ₹138.74 CPL, paused
- **C-2:** No pixel tracking, paused — ₹5,229 spent, 0 attributed leads
- **C-4 Retargeting:** ₹770.53 CPL, pool too small (2,235 people, freq 6.2), paused

### Winning Audiences (carried into C-6)
From C-1: Health Conscious, Millennials (Digital Natives — Netflix/Instagram)
From C-5: Indian Wellness & Fitness (Cricket/IPL/Yoga), Indian Digital Transactors (SBI/HDFC/Flipkart/Paytm)

### Paused Audiences
Travellers, Lives Away From Family, Family TV Viewers (from C-1)
Insurance & Health Risk Aware, Fitness & Wearable Users (from C-5)

### Geo Targeting
All Tier 1 cities: Mumbai, Delhi/NCR, Bangalore, Hyderabad, Chennai, Pune, Ahmedabad, Kolkata, Chandigarh, Ludhiana. Age 25-50.

## Funnel Data (PostHog — May 2026, ad-sourced path)
| Step | Users | Conversion |
|------|-------|-----------|
| Ad Landing Page Viewed | 2,174 | — |
| Phone Number Entered | 133 | **6.12%** (biggest leak) |
| OTP Verified | 115 | 86.5% |
| Onboarding Completed | 69 | 60% |
**Overall: 3.17% landing-to-lead. Avg time to convert: 1h 27m.**

## All-Time User Base (PostHog)
- March 2026: 47 onboarding completions
- April 2026: 45 onboarding completions
- May 2026: 203 onboarding completions
- **Total tracked: 295 users** (PostHog only goes back to March — pre-March users exist, website claims "1,000+ families")

## Key Problems Identified
1. **Landing page → phone entry: 93.88% drop.** Only 1 in 16 visitors attempts signup. Biggest lever in the account.
2. **App attribution gap:** 417 Play Store clicks from ads — none tracked in Meta. Real CPL is lower than reported.
3. **False iOS claim:** Website says "Works Everywhere: iOS, Android, Web" but iOS isn't live. App Store badge shows "Coming Soon." Damages trust.
4. **CTA confusion:** App Store + Play Store badges placed right next to the primary web signup CTA — distracts users at conversion point.
5. **Zero re-engagement:** No WhatsApp/email sequence post-signup. Week 2 retention near-zero in PostHog.
6. **No WhatsApp channel:** PostHog has no `whatsapp_clicked` events. WhatsApp doesn't exist in the funnel.

## Growth Strategy (3 Phases)

### Phase 1 — 1,000 Leads (4-6 weeks)
Priority actions:
1. Launch C-6 immediately (₹1,500/day)
2. Fix landing page: inline phone field, remove App Store distraction, fix iOS false claim
3. Fix Meta app attribution (SDK or server-side postback for app signups)
4. Cut C-3 to ₹50/day (retargeting pool not big enough yet, revisit at 20-30K engaged viewers in ~June)
5. Build Day 1/3/7 re-engagement sequence for post-signup users
Budget: ~₹1.82L | Target: ~162 leads/week at ₹100 CPL

### Phase 2 — 10,000 Leads (Month 2-3)
Precondition: C-6 proves ₹100 CPL over 3+ weeks
Actions:
- New creative: testimonial videos (Priya M./Rajesh K. on website already), problem-first hooks, AI demo screencaps
- New audiences: corporate IT employees, parents of school-age children, NRI/expat segment
- Budget required: ₹3-5L/month
Target: 3,000-5,000 leads/month

### Phase 3 — 50,000 Leads (Month 4-6)
Preconditions: Budget commitment, retention fix live, app attribution fixed
- Controlled Tier 2 test (₹200-300/day, 2-week comparison vs Tier 1)
- Google UAC (app campaigns) — high potential, untapped
- "Beta closing" urgency messaging if client approves
- Math: ₹50L total at ₹100 CPL. Requires serious budget conversation with client.

## Important Context for Strategy
- **Goal is investor traction**, not revenue. Lead volume + retention data = fundraising story.
- **Free beta continues indefinitely** — no paid launch planned.
- **Budget is tight** — client has not committed. Efficiency-first approach required.
- **No iOS app** — Android + web only. iPhone-heavy Tier 1 audience converts via web only.
- **Creative pipeline:** Can produce more. Dr. Tanvee is main face. Testimonials possible.
- **Tier 2 cities:** Do NOT expand yet. Test Tier 1 fully first. Lower CPM ≠ lower CPL guaranteed.

## Ad Landing Pages
- `/ad/responsibility` — "Still the one managing your parents' health?" (1,802 visitors in May — main page)
- `/ad/doctor` — 325 visitors in May

## Files / Reports Created
- `MeraHealth_CurrentStatus_May29.pdf` — 6-page current status report (C:\Users\soumi\OneDrive\Desktop\CLAUDE\Sessions\)
- `MeraHealth_May2026_UpdatedReport.pdf` — monthly Meta ads report (same folder)
- PostHog dashboard 1644231 — Acquisition Funnel (live, auto-updates)

## Instructions for Claude in New Sessions
1. Read this file at the start of any MeraHealth-related session
2. Check PostHog (project 351010) for latest funnel/retention data before making claims
3. Check Meta Ads (act_777565568463647) for latest campaign performance
4. Never assume budget has been committed — it's still tight
5. The #1 priority is always landing page conversion rate before scaling spend
6. Update this file whenever significant new data, decisions, or strategy changes occur
