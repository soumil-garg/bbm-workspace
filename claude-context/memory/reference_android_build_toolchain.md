---
name: reference-android-build-toolchain
description: "Android APK build toolchain installed 2026-10-11 under C:/cca/tools/android (JDK 17 + SDK platform 34 + build-tools 34); Swipe Desk app source and build script; signing key location; gotchas"
metadata:
  node_type: memory
  type: reference
---

Installed 11 Oct 2026 at Soumil's request ("create an APK for the swipe deck", then chose "Build here"): everything under `C:/cca/tools/android`, nothing system-wide, no env vars changed. Parts (all checksum-verified): OpenJDK 17.0.20.1 (adoptium zip, 191 MB) in `jdk17/jdk-17.0.20.1+1`, Android command-line tools 23.0 (commandlinetools-win-16111833, 155 MB) in `sdk/cmdline-tools/latest`, platform android-34, build-tools 34.0.0. Google's Android SDK license was accepted on his instruction. Setup script `scripts/setup_android.ps1` is idempotent (re-run to repair).

**Build an app:** copy `C:/cca/apps/swipedesk/build.ps1` as the pattern (aapt2 compile and link, javac --release 8, d8, add classes.dex, zipalign, apksigner, verify). Run it from a neutral folder: `powershell -NoProfile -ExecutionPolicy Bypass -File C:/cca/apps/swipedesk/build.ps1`. Output `build/Swipe-Desk.apk`.

**Signing key:** `C:/cca/tools/android/keys/swipedesk.jks` with password file `swipedesk.pw` (two identical lines because apksigner reads key-pass from the next line of the same file). Never print or share either. Losing the key means the app must be uninstalled before a re-signed update can be installed.

**Gotchas:** the new sdkmanager prints a deprecation warning on stderr (PowerShell with ErrorActionPreference Stop treats that as a failure, run it through cmd.exe and check exit codes); `Expand-Archive` is slow, use `tar -xf`; no emulator or phone here, so an APK is only verified structurally (apksigner verify, aapt2 badging, dexdump), never run.

**Swipe Desk app (11 Oct 2026):** package com.bbm.swipedesk, minSdk 24, target 34, no permissions, one launcher activity that opens `https://claude.ai/artifact/Uor2nfjf9ijzm9f9JYTzHp` with ACTION_VIEW (the Claude app if it handles claude.ai links, else the default browser; Chrome custom-tab extras added). It is a launcher, not an offline app: swipes still save into his Claude account (artifact db) and the 06:40 refill pipeline is unchanged. APK (50,140 bytes) sent to his WhatsApp self-chat KHoqSBX3WiSMP-fltKuvoA, message_id -5WzwD95W0-427UMKQtqWw. Source in `C:/cca/apps/swipedesk`. See [[project-swipe-desk]].
