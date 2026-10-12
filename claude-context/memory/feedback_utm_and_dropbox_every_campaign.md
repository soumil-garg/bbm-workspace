---
name: feedback-utm-and-dropbox-every-campaign
description: "Every Meta campaign for every brand must have UTMs utm_campaign={{campaign.name}}&utm_content={{ad.name}} and creatives must go via Dropbox"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 940e7931-a444-4748-869e-805e36a38dbf
  modified: 2026-10-01T02:20:29.990Z
---

Rule from Soumil (2026-10-01): on EVERY campaign, any brand, any new chat: (1) attach URL parameters `utm_campaign={{campaign.name}}&utm_content={{ad.name}}` to every ad, (2) upload creatives via the Dropbox flow ([[reference-dropbox-meta-upload]]).

**Why:** on Savvy I kept missing UTMs (used `{{ad.id}}`, or none on creatives built via the official connector). He called it a repeated failure. Also Pipeboard's free plan ran out mid-build.

**How to apply:**
- Official connector `ads_create_creative` has no url_tags and creatives are immutable. Use `ads_create_ad` with inline `creative` JSON including `url_tags` (works, Meta accepts it), or fix after the fact with Ads Manager bulk edit in Chrome Browser 2 (logged in to Facebook; Browser 1 is not): select ads, Edit, scroll to Tracking, URL parameters, Publish. Ads stay paused. Scroll with scroll_amount <= 10; screenshots sometimes time out, just retry.
- Never go hunting for Meta access tokens (blocked as credential exploration, and he does not have one set up).
- Always verify on one ad that the field shows the UTM string before saying done.
- The rule is also in global C:\Users\soumi\.claude\CLAUDE.md so it loads in any chat.
- Careful: Ads Manager "Review and publish" may hold unrelated draft items (9 Savvy video drafts with errors on 2026-10-01); do not publish them blindly.
