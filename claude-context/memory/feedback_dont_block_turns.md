---
name: feedback-dont-block-turns
description: "STANDING RULE 2026-10-07: never hold a turn open on long work; Soumil waits (often watching a movie) and cannot ask questions; launch long jobs in the background and hand control back"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 891b74f0-8beb-4d09-938f-31e9aa61b3c2
  modified: 2026-10-07T14:23:21.348Z
---

When a task takes more than about a minute, launch it as a background job (background agent, run_in_background shell command, Monitor) and END my turn with a one-line status and what will arrive. Do not chain waits, polling loops or long foreground tool calls (the 10-minute image build and my waiting loops on 7 Oct 2026 kept him stuck).

**Why:** Soumil said he sits watching a movie for 30 to 60+ minutes while I scrape or research, and cannot query me or redirect me, and he does not want a new session because his questions relate to the work in progress. Proof that the background pattern works: during the Amazon pull he asked about paid tools mid-run and I answered while the loop kept running.

**How to apply:** (1) background everything slow, one launch message, then stop; (2) when a task notification arrives, reply with one short line unless it needs him or finishes a milestone; (3) answer any question he asks from files and context while jobs run, without waiting for them; (4) cap concurrent agents (about 7 at once risked rate-limit cut-offs earlier); (5) tell him what is running and what each notification will mean. Related: [[reference_parallel_agent_runs]], [[feedback_tone]].
