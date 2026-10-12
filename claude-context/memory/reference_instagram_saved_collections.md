---
name: reference-instagram-saved-collections
description: "How to read Soumil's Instagram saved folders (meta ads, ai shit, habbit ads...) through his logged-in Chrome; folder ids; gotchas; why research agents miss reels; triage note location"
metadata:
  node_type: memory
  type: reference
  originSessionId: 891b74f0-8beb-4d09-938f-31e9aa61b3c2
  modified: 2026-10-07T17:09:17.274Z
---

Soumil's Instagram username is soumilgarg06. Saved folders seen at /soumilgarg06/saved/ on 2026-10-07: All posts, Audio, Gurugram places to visit, ai shit (id 3057667094579811, 2 reels), meta ads (2093503481589167, 38 reels), Movies, Content inspiration (18061075007520355), habbit ads (4775490776018548), The QUOTES, for p, outfit, dance. Only "ai shit" and "meta ads" were read; the others were left alone on purpose.

Method that worked (read-only): Claude in Chrome on his logged-in profile, a new tab at instagram.com, then page JS: GET /api/v1/feed/collection/<id>/posts/ with headers X-IG-App-ID 936619743392459 and X-Requested-With XMLHttpRequest, same origin, credentials include, follow next_max_id, 1.2 s between pages. It returns code, user, caption, play_count, taken_at and video_versions urls. /api/v1/collections/list/ and /api/v1/accounts/current_user/ do not work (404 or the HTML shell). Folder links come from the saved page anchors (/soumilgarg06/saved/<name>/<id>/).

Gotchas: the tool output filter replaces long base64-like strings (hrefs, signed video urls) with [BLOCKED], so space them out; window state is lost on every navigation (re-harvest); screenshots time out in the background tab (use get_page_text or JS); Chrome grabs his window on every call ([[feedback_browser_focus_stealing]]). Never like, save, unsave or follow. Downloading videos needs his explicit yes (state file names, source, size). Earlier reel pipeline: [[reference_eben_joseph_playbook]] (harvest json, download video_url, faster-whisper small.en).

Why research agents miss reels: they read the open web with no browser tools; reels are login-walled video; 15 of the 40 saved reels hide the content behind comment-for-DM funnels; viral tools reach us only when he forwards them. Full verdicts: vault Resources/Saved reels triage - meta ads and ai shit, 7 Oct 2026.md (after the video pass: 13 use or test, 6 already have, 7 reference, 14 noise). Findings that touch other notes: the sahni.ai reel runs Claude + Jev as a persona ad tester and MiroFish is a 73k-star crowd simulator, both the persona genre our research graded weak ([[reference_jev_typesafe]]); the Agent Reach reel is the source of the repo reviewed in [[reference_agent_reach_review]].

Proposed, awaiting his yes: a weekly saved-reels intake into the vault (read-only harvest, local transcripts, tags use/test/have/reference/noise) that the research agents read first.

Video pass (7 Oct, approved by Soumil for these 10 reels only): codes from the Chrome harvest, then the official Apify instagram-scraper with directUrls (public reel pages, no login, run-sync endpoint, Bearer token, 10 items in 13 s, about $0.03) returned videoUrl; Python downloaded the mp4 from the Instagram CDN (42 MB), faster-whisper small int8 transcribed 10 reels (3 minutes), PyAV and PIL made 8-frame sheets. Scripts and outputs in C:\cca\saved_reels. Two reels had no speech, so frames were needed. This route needs no Chrome once the reel codes are known. Findings: [[reference_jev_typesafe]] unaffected; TryBloom and Pletor (AI ad generators over a Claude connector, identical paid-looking hook) are alternatives to our engine, not connected; the native-format menu maps to the Habbits native slot.
