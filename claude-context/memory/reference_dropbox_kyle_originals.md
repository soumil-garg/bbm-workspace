---
name: reference-dropbox-kyle-originals
description: "How to pull files from Kyle's Dropbox share (Bad Marketing) without joining, what is in it, the vb2 builder and the 15 videos made 12 Oct 2026"
metadata:
  node_type: memory
  type: reference
  originSessionId: 455fe2db-0ead-4713-a975-bd719e7a8d39
  modified: 2026-10-11T19:36:28.876Z
---

Kyle's shared Dropbox "Bad Marketing" (link posted by Chelsea in the Lotus group, 11 Oct 2026; 14 top-level folders, "Soumil Videos & Photos" holds the videos, about 57 GB). Open it logged out in the built-in browser (decline cookies); read folder lists with get_page_text or a JS lister (the list is virtualised: scroll with the real wheel and re-read, and the pane must be fronted/visible or get_page_text times out).

**Download one file without joining:** `curl -sL -C - -o out "<subfolder share URL>?rlkey=<key>&preview=<url-quoted name>&dl=1"`; every sub-folder has its own token in the href (read it from the anchors in the browser). Speed was only about 1 MB/s on his connection, so never pull whole folders; pick files by name and sheet. Scripts: C:\cca\lotus-sculpture\originals\tools (dl.py, scan_dbx.py sheets/probe/transcribe, cuts.py, cropprev.py, strip.py, boards.py, finalize.py, write_note.py). Sources land in originals\dropbox_review\<folder>\. A file name with a stray space (201cs5 Sandstone Buddha Meditating.mov) returned an HTML page instead of the video.

**Builder:** research\ig\clips\vb2.py (any source size, cover or blurfit, band crop, push-in, captions styles cap/hook/chip/light/sky, music bed + the clip's own sound, end card) and plans_new.py (one function per video; music via music3.gen, one style per video). Run `python run1.py <plan> <9x16|4x5>` or `python plans_new.py <names>`. Builds are RAM-heavy (ffmpeg about 2.5 GB each): one at a time. Product titles go in the bottom chip, never a top banner, because orbit shots fill the frame and the banner covers the face.

**Result 12 Oct 2026:** 15 videos in videos_new\review (numbered, both sizes), boards, phone previews; list and flags in vault note lotus-sculpture-dropbox-review-oct2026. Unviewed by name only: about 80 more Instagram, travel and YouTube videos and the Arist buying trip, Clips for Gifs, Customer photos folders. Sold pieces skipped: 200ls1728, 200ls1729, 199ls1786.

Related: [[client_lotus_sculpture]], [[reference_miva_api_client]], [[feedback_dropbox_full_use_gdrive]].
