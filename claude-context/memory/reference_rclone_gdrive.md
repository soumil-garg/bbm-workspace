---
name: reference-rclone-gdrive
description: rclone setup for pushing large local files to the Masters Union Google Drive (1TB+ EDU account)
metadata: 
  node_type: memory
  type: reference
  originSessionId: 85548897-59e5-4aa4-a662-8ede1e155c89
  modified: 2026-09-02T08:23:05.102Z
---

rclone v1.75 installed at `C:\Users\soumi\Tools\rclone\rclone.exe` (portable, no admin).

Remote name: **`mu_drive`** — authorized against the **Masters Union college Google Workspace account**, NOT personal soumilgarg1111@gmail.com. Confirmed 360 TiB pooled quota / ~34 TiB free, so large uploads are a non-issue there. Config at `C:\Users\soumi\AppData\Roaming\rclone\rclone.conf`.

One-click resume script: `C:\Users\soumi\Tools\rclone\resume-upload.cmd` — runs `rclone move` of `C:\Users\soumi\Videos\Screen Recordings` to `mu_drive:Screen Recordings`. Skips already-uploaded files, deletes local copy only after Google confirms a matching checksum. Safe to re-run any number of times.

Caveats:
- Uses rclone's **shared Google client_id, being retired during 2026** and already rate-limited (hit a 403 during setup). For durable use, create a private OAuth client ID in Google Cloud Console.
- `rm`/rclone deletes bypass the Windows Recycle Bin — permanent. The Drive copy is the only backup, and Drive trash auto-purges after 30 days.

Machine context: C: is a 476 GB drive that runs at 96-100% full. `pagefile.sys` balloons to ~22 GB under Chrome memory pressure (16 GB RAM, Chrome routinely holds ~5 GB), which eats reclaimed space. `hiberfil.sys` is another 6.4 GB — `powercfg /h off` from an admin shell frees it. Screen recordings were never the real disk problem; ~425 GB is something else, still unscanned.

See [[user-name]].
