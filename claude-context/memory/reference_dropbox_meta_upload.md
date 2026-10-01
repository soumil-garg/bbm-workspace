---
name: reference-dropbox-meta-upload
description: How to get local videos into Meta via Dropbox (Pipeboard) — folder path + sync gotcha
metadata:
  node_type: memory
  type: reference
  originSessionId: 5a5f0c96-87fc-467f-8b6d-89a7fd717b91
  modified: 2026-09-24T23:08:59.352Z
---

Pipeboard's Dropbox connection = the local Dropbox at C:\Users\soumi\Dropbox (full-access paths, e.g. `/Apps/BBM Creatives/<client>`).
Flow: download Drive folder with `python -m gdown --folder <url>`, copy into `Dropbox\Apps\BBM Creatives\<client>`, then `create_creatives_from_dropbox_folder` or `upload_ad_video_file` with the path.
Gotcha (2026-09-25): Dropbox desktop client hung and silently stopped syncing; killing + restarting Dropbox.exe fixed it. Large files (~100MB) take several minutes each to sync; upload per-file as they land.
Savvy Body Glue: act_1739758317082177, page 1296421220224810, pixel 972185532584331, campaign 120252656261330270.
