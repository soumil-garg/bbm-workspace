---
name: project-daigo-retainer-upgrade
description: "Daigo retainer upgrade 2026-10-09: BBM takes over ad creatives and website changes, Rs 40,000 a month; v1 text 9 Oct, v2 illustrated PDF + artifact 10 Oct (not sent, Soumil sends)"
metadata:
  node_type: memory
  type: project
  originSessionId: 808b8024-6187-44e8-9ba9-79b0fccab1e6
  modified: 2026-10-09T12:56:01.050Z
---

Meeting with Daigo founder Manan on 2026-10-09: BBM will handle ad creatives and website changes on top of media buying. Price was not agreed in the meeting. Soumil's decision afterwards: charge Rs 40,000 a month in total (existing Rs 20,000 + Rs 20,000 extra). Scope in the proposal is ONLY ad creatives and website changes. WhatsApp campaigns are a future additional service and must NOT be mentioned in the proposal.

**Why:** the client was slow to supply creatives (gaps of 17 to 75 days between batches); the 28 Sep AI statics batch lifted sales (see [[client-daigo]] and the impact report in Daigo/Reports).

**How to apply:** when the meeting transcript arrives, draft the proposal for Manan using the transcript plus the report data. Plain, positive wording per [[feedback-client-comms-simple-positive]]; first person singular per [[feedback-solo-voice-first-person]] if it fits. Do not send; Soumil sends himself unless he asks.

**10 Oct 2026, v2 built (illustrated, 4 A4 pages):** `Sessions\Daigo\Proposals\Daigo_Proposal_Creatives_Website_Oct2026.pdf` (+ `.html`), private artifact https://claude.ai/artifact/DbrDm8iC4dzdvavmqPnevp, build folder `C:\cca\daigo\proposal\` (build_proposal.py computes every number from assets/daily.json; refresh = swap daily.json, run script, run render.ps1). Includes the first four round 4 creatives (numbers 1 to 4, not live, not yet seen by Manan). Not sent; Soumil sends it himself.
- Headline leads with volume (+47% sales a day, 13.4 to 19.6); "at a lower cost" was dropped from the headline because the research note calls the efficiency change noise (CAC Rs 212 to Rs 188 stays as a supporting figure with a caveat). It is 47%, not the 46% in v1. Spend per day rose 30%, said openly.
- Navratri dropped from the festival example (banned in Daigo copy, starts 11 Oct); Diwali stays.
- Ad-level figures use the impact report window (29 Sep to 7 Oct, 39 of 48); account level runs to 8 Oct.

**11 Oct 2026:** Soumil set the split of the Rs 40,000: Rs 20,000 media buying (current) + Rs 15,000 ad creatives + Rs 5,000 website and CRO. Proposal PDF/HTML/artifact updated (fee bar plus three priced cards, dated 11 Oct; first version in `Proposals/Archive/`). He asked what 7, 10 or 15 creatives a week costs per creative (Rs 536, Rs 375, Rs 250 on a 4-week month) and the pros and cons; my recommendation is 10 a week (7 new + 3 remakes of last week's best), because the limit is test budget (a fair look is about Rs 500 an ad; 15 a week would eat 89% of the Rs 8,400 a week test budget) and fresh ideas, not production. His pick is pending; the proposal still says "10 to 15" in four places. Numbers and table are in the vault note `daigo-retainer-proposal-oct2026`.

**11 Oct 2026, send scheduled:** Soumil asked me to send the proposal PDF in the Daigo WhatsApp group "tomorrow at 10am" (said at 1 AM, he then chose Sun 11 Oct 10:00 AM IST). Scheduled task `send-daigo-proposal-oct11` (one time, fireAt 2026-10-11 10:00 +05:30) sends `Proposals/Daigo_Proposal_Creatives_Website_Oct2026.pdf` with a one-line caption to group chat `-mhrWX32XAeWluCGLKp66g` (see [[whatsapp-api-read-only]]). Needs the Claude app open at 10:00 and Soumil's one-click approval on the WhatsApp guard prompt (guard not bypassed). Never press "Run now" on it, that sends immediately. If the PDF is regenerated before 10:00 the task sends the new file (same path).

**11 Oct 10:30 correction:** the 10:00 send did NOT happen. The Claude app was closed at 10:00, the task started at 10:19 and its first tool call was interrupted by Soumil, so nothing was sent (he posted "Ad budget low" in the group himself at 10:20, Manan replied "done"). He then said "send tomorrow at 10": new one-time task `send-daigo-proposal-oct12` (fireAt 2026-10-12 10:00 +05:30, checks in one read-only command, stops if any tool use is declined); the old task `send-daigo-proposal-oct11` stays disabled. Needs the Claude app open and the laptop awake at 10:00, and up to two approval clicks (pre-send check, send). Never use "Run now" on it (sends immediately). The PDF still says 11 Oct and numbers to 8 Oct; refresh only if he asks.

**12 Oct 2026 (about 14:30): SENT.** At his request, right then, the PDF went to the Daigo group with the text "Hi Manan bhai, as per our last discussion, this is the new proposal." (message_id aZdU-g2FXsiMOF6EoXWFYQ). The Mon 10:00 scheduled task had stalled on its first approval prompt (nobody at the screen) and was stopped; both Daigo send tasks are now spent. Lesson: scheduled WhatsApp sends stall without someone to click the guard prompt, so for a time-critical send either be at the machine or send live. Open next: Manan's reply, then the weekly volume pick (7, 10 or 15) and the "10 to 15" wording in the proposal.
