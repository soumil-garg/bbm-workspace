---
name: client-mufasa
description: "Mufasa Man (mufasaman.com, deo sticks + perfumes) Meta account IDs, 2026-10-07 deo video launch, and the Dropbox-temp-link video upload route that bypasses Pipeboard"
metadata:
  node_type: memory
  type: project
  originSessionId: 12113d1f-868a-4fa0-a52a-c87ad7ec6f56
  modified: 2026-10-07T08:50:06.286Z
---

Account `611633726787161`, page `101618088696712`, pixel `5269979343095866`. Site mufasaman.com, code MM10 (extra 10%, free shipping, verified live 2026-10-07). Deo sticks at /collections/deo-sticks (/products/oud-deo-stick, /products/aqva-deo-stick, both Rs 1,053 after 10% tag). Account convention: headline `Extra 10% off, Code- "MM10"`, CTA ORDER_NOW, Bihar (region key 1752) excluded, India 18-65, Advantage+ audience, pixel PURCHASE.

**Launch 2026-10-07 (Soumil: "Launch it at Rs 1,000, new campaign, go"):** campaign `120248385260170018` Mufasa_DeoVideos_CBO_07Oct (CBO Rs 1,000/day), ad set `120248385268510018` excluding audience `120248385109580018` (Website Visitors 60D, ALL_VISITORS), ads V1_TravelBag 120248385279080018, V2_LastToKnow 120248385279280018, V3_PerfumeAsDeo 120248385279410018. Videos are Salaj's Oct 6 deo-stick videos. All point to the deo-sticks collection page (not a product page; existing ad destinations could not be read).

**Why:** Pipeboard's paid plan caps 3 distinct ad accounts per month (Habbits, Bagwani, Lotus took them; Mufasa blocked until 2026-11-06). See [[project-pipeboard-plan-seats]].

**How to apply:** for Mufasa video or image upload use the Meta connector `ads_creative_upload_media` with `upload_source: URL` and a Dropbox temp link (Dropbox API get_temporary_link, ~4h, app root = "BBM Creatives"); it returns video_id / image_hash. Upload a 1080x1920 thumb as IMAGE for `image_hash` in video_data. UTMs cannot be read back through the Meta connector (no url_tags field on ads_get_creatives); verify in Ads Manager or via Pipeboard when a seat is free.

Related: [[reference-dropbox-meta-upload]], [[feedback-scope-salaj-only]]
