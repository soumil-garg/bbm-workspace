---
name: reference_laptop_quirks
description: "Soumil's laptop specs and quirks (RAM nearly full, many Chrome profiles, Brave runs from a non-standard folder); read before installing software or diagnosing slowness"
metadata:
  node_type: memory
  type: reference
  originSessionId: 4618a210-fb15-41b1-b925-84a04c1f5af7
  modified: 2026-10-05T00:31:43.189Z
---

Laptop: Acer Swift Go 14 (SFG14-71), Intel i7-13700H, 15.7 GB RAM, Windows 11 Home Single Language build 26300 (Insider-type build), 476 GB disk. On 5 Oct 2026 RAM was 88 percent used in normal work (Chrome 38 processes about 5.5 GB, Claude app about 2 GB, plus Wispr Flow, Notion, Dropbox, Proton VPN client), and it was often on battery in Balanced mode, which slows the CPU. Chrome has about 25 profiles; Profile 5 (26 extensions: Dark Reader, Grammarly, GMass, lemlist, PhantomBuster, React DevTools and more) and Profile 1 (20 extensions: Grammarly, Helium 10, Lusha) are the heavy ones. No Chrome crashes in the Windows log. He asked why Miva admin lags in Chrome; the advice was to test in a clean browser with no extensions.

Quirk: per-user Chromium installs fail to start from inside AppData\Local with "side-by-side configuration is incorrect" (Brave 154.1.96.61, event SideBySide id 33), even a fresh copy there; the same files run from a normal folder. Brave therefore lives at C:\Users\soumi\Brave\Application\brave.exe with a Desktop shortcut (Brave.lnk); it will not auto-update. Proper fix offered: a system-wide install into Program Files (needs his UAC approval), as Chrome is. The broken install in AppData\Local\BraveSoftware\Brave-Browser (about 1 GB) was left in place pending his decision.

**How to apply:** do not run `chrome.exe --version` to test (it opens a window in the existing session); sxstrace and system-level installs need an elevated session, which the tool session does not have; the shell tool blocks Remove-Item on paths directly under C:\.
