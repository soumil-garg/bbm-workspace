---
name: reference-agent-reach-review
description: "Soumil sent himself the GitHub link Panniantong/Agent-Reach on 2026-10-07; reviewed (read-only): legitimate-looking repo, verdict SKIP for our stack; risks and what it would add"
metadata:
  node_type: memory
  type: reference
  originSessionId: 891b74f0-8beb-4d09-938f-31e9aa61b3c2
  modified: 2026-10-07T16:00:58.233Z
---

Link: https://github.com/Panniantong/agent-reach (Facebook fbclid tracking tag on the shared URL, harmless). "Give your AI agent eyes": a capability layer that installs and wires up other tools (Jina Reader, yt-dlp, twitter-cli, rdt-cli, OpenCLI, bili-cli, mcporter + Exa MCP, gh). MIT; created 24 Feb 2026; 93k stars, 8.1k forks; last release v1.5.0 (Jun 2026), last push 15 Sep 2026; owner account from 2020 (38 repos); README in Chinese with sponsor ads (BrowserAct, CoreClaw, Tencent Cloud).

Read-only review by me (GitHub API, no clone, no install): code scan found no obfuscation, no eval or exec, no shell=True, no curl-pipe-shell, no telemetry, expected hosts only (github, mcp.exa.ai, r.jina.ai, groq, bilibili, v2ex, xueqiu). Not a professional audit.

Concerns: (1) install flow is "paste this link to your AI agent" and installs unpinned from the main branch zip; `--system` mode runs npm -g and pip via subprocess; it can register a SKILL.md into ~/.claude/skills (persistent instructions); the README warns the same-name PyPI package is NOT this project (squat risk). (2) Reddit, Instagram and Facebook have no zero-config path: they reuse the user's logged-in Chrome through OpenCLI (a separate third-party npm package `@jackwener/opencli` plus a Chrome extension and a local daemon on 127.0.0.1:19825), or rdt-cli extracts browser cookies; `cookie_extract.py` uses browser_cookie3 for Chrome, Firefox, Edge, Brave, Opera. That uses Soumil's personal accounts (ban risk, credential exposure); the docs themselves advise a secondary account. (3) Instagram support is user search, profile and a user's recent posts, NOT hashtag or keyword post search; Facebook only a groups list; Reddit needs login.

Verdict: SKIP. It adds little over the paid Apify, DataForSEO and ScrapeCreators plan ([[reference_scraping_tools_oct2026]]) and conflicts with the rule not to use his personal accounts for scraping. Useful pieces exist on their own: yt-dlp (transcripts), Jina Reader (r.jina.ai), Exa MCP free tier. I cannot install third-party code for him; if he insists, he runs it himself in an isolated user or VM with throwaway accounts.

Related: [[reference_amazon_review_pull]], [[reference_whatsapp_api]].
