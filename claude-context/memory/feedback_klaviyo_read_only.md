---
name: feedback-klaviyo-read-only
description: "STANDING RULE (2026-10-07): Lotus Klaviyo is connected for DATA ONLY; never create, edit, send, pause or change anything in Klaviyo; aggregates only, no profile lists"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 8049c016-5a38-42db-970c-1abc40055ec0
  modified: 2026-10-07T04:19:45.338Z
---

Klaviyo (Lotus Sculpture account YrL3Tk) is connected through the official connector (tool names mcp__5fd17b08-...). Use it to read data only.

**Why:** 2026-10-07 Soumil: "under any circumstances, I don't want you to change anything, create a new campaign, or edit the existing campaign for Klavio. That is just there to help you with data." Lotus runs live email and SMS campaigns there and customer data is covered by the NDA.

**How to apply:**
- Only get_, list_, query_ and report calls. Never call anything that creates, updates, sends, schedules, pauses, suppresses or deletes, even if a tool for it appears later. render_email_template is read only but not needed.
- Aggregates only (get_campaign_report, get_flow_report, query_metric_aggregates). Do not pull profiles, emails or phone numbers.
- Useful ids: Placed Order metric V2m95P (clean second order count, matches Miva). Reports are large; they save to a tool-results file, parse with Python.
- Findings are in vault Projects/lotus-sculpture-klaviyo-picture-oct2026. See [[client_lotus_sculpture]] and [[feedback_tracking_audit_first]].
