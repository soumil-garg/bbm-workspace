---
name: reference-openai-key-rotation
description: "OpenAI key lives only in the user env var OPENAI_API_KEY; rotate with C:/cca/tools/set_openai_key.ps1 (clipboard, validated, never in chat); scripts read the registry first; rotated 2026-10-10 after credit_balance_exhausted"
metadata:
  node_type: memory
  type: reference
  originSessionId: b3607133-6288-42df-85dd-d0d6d53e5a58
---

**Where it lives:** only in the Windows user environment variable OPENAI_API_KEY (HKCU Environment). No machine-level copy, and no copy in scripts, configs, skills, memory or the vault (checked 2026-10-10).

**Rotate:** he copies the new key, then runs `powershell -NoProfile -ExecutionPolicy Bypass -File "C:/cca/tools/set_openai_key.ps1"`. It reads the clipboard, checks the key with a free models call, replaces the variable and prints only the last four characters of each key. Never take a key in chat: it would stay in the transcript, and entering keys is his action.

**Why the readers look at the registry first:** a running Claude session keeps the key it started with in os.environ (it stays the old key until the app restarts). Since 2026-10-10 `gen_image.key()`, `theme_counter.getenv`, `jev_client.getenv` and `lotus-sculpture/oai.key()` read the registry first, so a rotation works at once for my scripts, the Swipe Desk refill and the Jev tests. Apps already open (the Claude app, MCP servers) keep the old value until restarted.

**Verify spend:** one gpt-5-mini chat call with reasoning_effort minimal and max_completion_tokens 64 costs about $0.00002; HTTP 429 insufficient_quota or credit_balance_exhausted means the account has no credit.

**2026-10-10:** the old key (ended brsA) hit credit_balance_exhausted. Soumil made a new key (ends vbsA), set it with the script, and it passed the spend test. He deletes the old key on OpenAI's keys page. The ledger `C:/cca/_ledger/balance.json` is a manual estimate: set start_usd and as_of (ISO datetime) when he states the credit. Done 2026-10-10 19:58: he credited $5, start_usd 5.00. Related: [[feedback-whole-ad-generation-harmony]], [[project-daigo-pilot-oct2026]], [[feedback-ground-spend-caps]].
