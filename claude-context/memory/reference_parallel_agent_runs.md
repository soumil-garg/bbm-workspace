---
name: reference-parallel-agent-runs
description: How the 6-agent Lotus analysis was run on 6 Oct 2026 and what worked or broke; reuse for any multi-agent analysis
metadata:
  node_type: memory
  type: reference
  originSessionId: 4618a210-fb15-41b1-b925-84a04c1f5af7
  modified: 2026-10-06T06:33:53.446Z
---

Pattern that worked (Lotus full analysis, 6 Oct 2026, six general-purpose agents in parallel): write ONE shared brief file (C:\cca\lotus-sculpture\analysis\_AGENT_BRIEF.md: client facts, hard rules, read-only, NDA, tag findings Confirmed/Likely/Hypothesis, output contract) and keep each agent prompt to its own tasks; one output folder per agent; each agent returns a 1,000-word digest, detail stays in CSVs and scripts. The lead then re-checks the headline numbers independently (35 of 35 and the lead's own recompute matched) before quoting them.

What broke or needed care:
- The harness refuses most subagent writes of REPORT.md ("subagents should return findings as text"). Ask for findings as the final message plus CSVs and md tables with other names; do not expect REPORT.md.
- A run interrupted by an API error keeps its files and its transcript: resume with SendMessage to the agent's agentId (not a new Agent call). Tell it to inventory its folder, not redo work, update its write-up after each task, and give a priority order.
- Cloudflare-protected client sites block every scripted route (built-in browser, WebFetch, requests); agents cannot verify live offers, so plan a real-browser pass by Soumil, ideally from the client's country.
- Shared resources are consumed by several agents at once (Apify free credit, Meta connector calls: Pipeboard free plan ended after 28 calls, the official connector has no attribution-window option). Name a budget per agent.
- Agents that download images can balloon a folder (ads_site\competitors\img reached 795 MB); say a download cap.
Related: [[client_lotus_sculpture]], [[reference_apify]]
