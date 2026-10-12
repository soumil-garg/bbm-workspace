---
name: client-eora
description: "Eora Skincare (myeora.in) Meta account facts, 2026-10-08 new video campaign, expired PAYDAY20 sale ads still live, Pipeboard seat swap used"
metadata:
  node_type: memory
  type: project
  originSessionId: 12113d1f-868a-4fa0-a52a-c87ad7ec6f56
  modified: 2026-10-08T13:18:55.180Z
---

Ad account `1442450130603789` (Eora.In), page `1019130427946712`, pixel `4501479360097928`, group chat id `jgOFofIxV1WKQTsUPFz-8Q` (WhatsApp resolver labels it "Salaj"; the Eora client founder Sakshe is in it). Hero product: Moisture Drench Body Wash (Rs 1,200, /products/moisture-drench-body-wash). Code HYDRA10 = 10% off first order (site banner, verified 2026-10-08). Old audiences used for exclusions: WV-180 (120251903318500380), Purchasers_730D (120251767819280380), ATC_180D (120251767823680380), IC 180D (120251767810130380).

**Launched 2026-10-08 (Salaj named Soumil, 13:32 IST):** campaign `Eora_NewVideos_CBO_08Oct` 120252218232610380, Rs 1,000/day CBO; ad set `PAN-India_ExclOldAudiences` 120252218235460380 with the four exclusions; 3 ads: 1_Reel1_FounderStory_HYDRA10 120252218515800380, 2_Reel2_HonestPrice_HYDRA10 120252218516180380, 3_Freg7_UGC_HYDRA10 120252218516890380. Influencer Instagram reel (client: download and post separately, never run ads on the influencer's account video) NOT done. Niki Mehra ad `Influencer video ads awareness` 120251884885650380 paused 2026-10-08 17:59 IST.

**Still open:** ads `Self care UGC` and `Slow Morning` in CBO_ShowerGel_Videos_5th Aug still say "20% OFF Ends 4th Oct, Use PAYDAY20" (creatives are immutable, replace with a HYDRA10 headline and body; Self care UGC body also says 4-day payday sale). Salaj's DM 13:34: change that headline to Hydra 10. Someone else holds 3 unpublished Ads Manager drafts in this account (HydratingDuo_Static_01 rename, Care beyond your face creative, BOF_WV180 ad set edit): never publish them.

**How I got videos in (why it matters next time):** the Meta connector `ads_creative_upload_media` is gated for Eora ("gradually rolled out"); Chrome file pickers and localhost fetches do not work; Pipeboard `create_creatives_from_dropbox_folder` (param `dropbox_folder_path_or_id`) works once the account has a seat. 2026-10-08 Soumil did the one-time Pipeboard re-pick: seats now Bagwani, Lotus Sculpture, Eora; Habbits removed and Mufasa still blocked until 2026-11-06 (see [[project-pipeboard-plan-seats]]).

**Publishing from Ads Manager:** API edits/creates are staged as drafts; `ads_activate_entity` can refuse to publish if any draft in the account has an error. Fix: Ads Manager, Review and publish, tick only my own rows and publish (Chrome via Claude in Chrome worked). A paused ad set edit made via the API stayed a draft until published this way.

Related: [[client-mufasa]], [[feedback-scope-salaj-only]]
