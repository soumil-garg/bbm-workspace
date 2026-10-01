---
name: reference-meta-cta-share-ads
description: Meta API returns an empty call_to_action_type for existing-post (SHARE) ads even when a CTA is set — empty never means missing
metadata: 
  node_type: memory
  type: reference
  originSessionId: 6f3a8b0b-df8c-42f3-a8fc-34f5007a86d2
  modified: 2026-09-04T13:03:40.058Z
---

When auditing ad CTAs via `ads_get_creatives`, a creative with `object_type: "SHARE"`
(an "use existing post" ad, identifiable by `effective_object_story_id` /
`effective_instagram_media_id`) returns **no `call_to_action_type` field at all** — even
when a CTA is set and rendering fine in Ads Manager.

The button lives on the underlying Page/Instagram post, not on the ad creative, so the
API simply has nothing to report at the creative level.

**Do not report these as "CTA missing."** Confirmed 2026-09-04 on Mufasa Man ad
"Sweat happens" (`120247803366440018`, creative `1644822147204334`): API returned no CTA,
Ads Manager showed "Order now" set correctly. I flagged it as a possible gap and it was a
false positive.

If a CTA audit needs to cover SHARE ads, the creative object is a dead end — check the ad
preview, or resolve the post via `effective_object_story_id`.

Related: [[process_ad_creatives]]
