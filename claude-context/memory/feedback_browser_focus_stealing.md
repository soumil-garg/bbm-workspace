---
name: feedback-browser-focus-stealing
description: "Soumil's active window gets yanked to the browser tab Claude is driving; Claude in Chrome does this on every tool call (upstream bug). Default to the built-in browser and minimise Chrome calls."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 6f3a8b0b-df8c-42f3-a8fc-34f5007a86d2
  modified: 2026-10-06T03:59:20.591Z
---

When Claude works in a browser, Soumil's current window is switched to that tab/window. Reported 2026-10-06 ("Fix that").

**Why:** The Claude in Chrome extension (`mcp__claude-in-chrome__*`) brings its tab group to the foreground on every tool call. It is a known upstream regression since about 26 Mar 2026 (GitHub anthropics/claude-code issues 31119, 39600, 39707). The desktop app's Code settings (ccd_settings) have no toggle for it. Changing Windows foreground-lock settings is a system setting, so never do it.

**How to apply:**
- Default to the built-in browser (`mcp__Claude_Browser__*`, the Browser pane). It is isolated from his Chrome and does not steal his window.
- Use Claude in Chrome only when a logged-in session is needed (Uphill Google Sheets and Drive, Miva, Ads Manager under his login). Say so before starting.
- Keep Chrome work to as few calls as possible: one `browser_batch`, or one `javascript_tool` fetch/read, instead of many clicks and screenshots. Never loop screenshots.
- Prefer APIs and MCPs over the browser when they exist (Meta Ads MCP, WhatsApp API, Shopify screenshots from him).
- Hidden windows ignore keystrokes and screenshots time out, so a Chrome write needs his window visible. Ask him to bring it forward, then do it in one burst.

Related: [[feedback-send-when-asked]] (no permission nagging; send when he asks).
