---
name: feedback-placement-asset-customization
description: "When a creative has multiple aspect ratios, build ONE ad with placement asset customization, never one ad per format; how to do it via Meta MCP"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a2f8c560-441b-42b0-b333-48adbf668e99
  modified: 2026-09-14T11:35:18.210Z
---

When the same creative comes in multiple formats (1:1, 4:5, 9:16), build a single ad with placement asset customization: vertical asset in Stories/Reels, square/feed asset in Feeds. Never split it into separate ads per format.

**Why:** On 2026-09-14 I built the Daigo Ganesh Chaturthi campaign as two ads (1x1 and 4x5) of the same design. He called it a mistake: it splits budget and learning across what is really one ad.

**How to apply:**
- `ads_create_creative` only supports placement customization for video (`placement_videos`), not images.
- For images, it works through `ads_create_ad` with an inline `creative` JSON:
  - `object_story_spec` holds only `page_id` + `instagram_user_id`.
  - `asset_feed_spec` holds `images` with adlabels, `bodies`/`titles`/`link_urls` with adlabels, `ad_formats` `["SINGLE_IMAGE"]`, and `optimization_type` `PLACEMENT`.
  - `asset_customization_rules` needs two rules:
    - Priority 1: `customization_spec` `{publisher_platforms:[facebook,instagram], facebook_positions:[story,facebook_reels], instagram_positions:[story,reels]}` gets the vertical image.
    - Priority 2: empty `customization_spec` `{}` is the default and gets the feed image.
- Verified working on Daigo ad 120256051142110460.
- Caveat: the inline path cannot set `self_ai_disclosure`. Flag this to him.
- Verify the placement mapping by loading each preview_url in the Browser pane and reading image `naturalWidth`/`naturalHeight` via JS. Screenshots fail when the window is minimized.
- Ads Manager in Claude in Chrome hangs on the Ad creative module (script injection timeouts, extension disconnects). Prefer the API path.

Related: [[client_daigo]]
