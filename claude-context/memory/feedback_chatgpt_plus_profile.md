---
name: feedback_chatgpt_plus_profile
description: "Before ANY ChatGPT image generation, verify the Chrome profile is the ChatGPT Plus one. Browser 1 / Browser 2 numbering changes between sessions."
metadata:
  node_type: memory
  type: feedback
  originSessionId: 738256e6-23ea-49a8-936c-84a31330a1b8
  modified: 2026-10-01T05:47:56.467Z
---

Soumil has two Chrome profiles. Only one is ChatGPT Plus (soumil@uphillads.com). The other is a Free account (shows "Soumil Garg / Free" in the ChatGPT sidebar, with a "Claim offer" button) and may also be in use by another Claude session (a Mufasa chat was open there). The "Browser 1 / Browser 2" labels and deviceIds are NOT stable across sessions.

**Why:** On the Lotus Sculpture ads (2026-10-01) I started generating on the Free profile without checking and he was furious: "are u nuts, we have to use the chatgpt plus one". Free limits image generation and the output is not comparable.

**How to apply:** Before touching ChatGPT: open chatgpt.com in the selected browser, read the plan label in the sidebar footer or account menu, and confirm it says Plus (or Pro). If it says Free, switch browser (list_connected_browsers, select_browser) and re-check. Never paste into a chat that is not mine (another session's chats can be open; chatgpt.com can resume the last chat, click New chat). Related: [[reference_chatgpt_image_pipeline]] [[process_ad_creatives]].
