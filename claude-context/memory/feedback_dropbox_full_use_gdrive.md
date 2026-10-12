---
name: feedback-dropbox-full-use-gdrive
description: Dropbox storage is full; share review folders through his personal Google Drive, not Dropbox
metadata:
  type: feedback
---

On 2026-10-10 Soumil said Dropbox storage is full and he does not want me to overuse it. He has about 5 TB on his personal Google Drive and wants review uploads (for example the Lotus videos before they go to Kyle) there. He agreed to connect a Google Drive connector.

**Why:** Dropbox quota is exhausted, so a 950 MB upload could not finish, and his Dropbox is shared with the Meta creative flow.
**How to apply:** stage files under C:\cca first; put review folders in his personal Google Drive; the rclone remote mu_drive is the Masters Union college account and is never used for client work. The Google Drive connector uploads file bytes inside the call, so it is fine for small files but not for hundreds of MB: for large uploads use rclone authorised to his personal account (he signs in himself) or Drive for desktop. Copy to Dropbox only for the Meta upload flow, one client at a time, and clean up after. See [[reference-rclone-gdrive]] and [[reference-dropbox-meta-upload]].

**Update 2026-10-11:** checked dropbox.com (logged in on his Chrome, Dropbox Basic free 2 GB): after my 950 MB review folder was moved out, usage is 1 GB of 2 GB, so it is no longer full. The 1 GB is all Apps\BBM Creatives (75 files): savvy videos about 730 MB (25 Sep), Bagwani, Mufasa Oct6 and Eora Oct8 videos about 200 MB, plus statics for Savvy, Daigo, Habbits. Nothing was deleted. Do not add Chelsea's shared "BAD Marketing" folder to his Dropbox (shared folders count against his quota once added); open it in the browser and download only what is needed. If he wants space back: archive to his personal Google Drive first (rclone gdrive_personal), verify by checksum, then remove from Dropbox.

**Lotus "Bad Marketing" Dropbox folder (11 Oct 2026):** shared from the info@lotussculpture.com Dropbox (name "kyle tortora") with invitation email to soumilgarg1111@gmail.com (edit access, sent 10 Oct 23:31 IST, "all of our marketing material, including IG reel and YouTube videos"; the group message says the useful subfolder is "Soumil Videos & Photos"). His Dropbox login in Chrome is soumilgarg0888@gmail.com, so the link shows "Request access" (1111 was given access, signed in as 0888). Not fixed: needs either Kyle/Chelsea to share to 0888 or send a view/download link, or Soumil signing in to a Dropbox account for 1111 himself. I must not create an account or enter his password, and clicking Request access messages the owner (needs his go). Never "Add to Dropbox" (counts against his 2 GB).

**11 Oct 2026 later:** Soumil signed Chrome into a NEW Dropbox account for soumilgarg1111@gmail.com (empty, 2 GB). The shared folder "Bad Marketing" is 57 GB, so Dropbox says "Not enough space to access folder" (Shared > Folders: "You haven't joined this folder"); it can't be browsed or mounted on a free account. Fix: ask Lotus to send a shared link (or share only the subfolder "Soumil Videos & Photos"), because links can be browsed and downloaded without joining. Do not buy a plan for him. Chrome's Dropbox login is now 1111; the laptop's Dropbox desktop app is still the 0888 account.
