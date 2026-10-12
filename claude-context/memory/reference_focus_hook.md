---
name: reference-focus-hook
description: Stop and Notification hook focus-claude.ps1 pauses video (not music) and pulls the Claude window forward; how the music vs video rule works and how to tune it
metadata:
  node_type: memory
  type: reference
  originSessionId: 6f3a8b0b-df8c-42f3-a8fc-34f5007a86d2
  modified: 2026-10-06T01:36:26.268Z
---

`~/.claude/settings.json` runs `C:\Users\soumi\.claude\scripts\focus-claude.ps1` on every Stop and Notification event. It reads Windows media sessions (SMTC), pauses playing browser/player VIDEO, and brings the Claude desktop window to the front.

**2026-10-06 change (Soumil's request):** music must keep playing, Claude still takes focus. Chrome always reports PlaybackType=Music, so that flag is useless. A session counts as MUSIC if any of: it has an album, the source app is a music app, it is 7.5 minutes or shorter, or the title or channel matches the `$MusicWords` regex (music, lofi, playlist, Topic, T-Series, Saregama, ...). Everything else playing in a browser or player is treated as VIDEO and paused. When unsure it leaves media playing, because cutting music is the annoying mistake.

**Tuning:** every decision is appended to `~/.claude/scripts/focus-claude.log`. If a video is not paused, or music is, add or remove a word in `$MusicWords` or change the 7.5 minute cut. `-Selftest` runs sample titles and `-DryRun` shows live sessions without pausing or focusing. Original is `focus-claude.ps1.bak-2026-10-06`.

**Known gap:** a short YouTube clip (7.5 minutes or less) with no music words is left playing, and a long music upload with no music words in the title or channel gets paused.

Related: [[feedback-browser-focus-stealing]]
