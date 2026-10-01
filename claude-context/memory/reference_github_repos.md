---
name: github-repos
description: Where the public skill repo and private client-work/context repo live, and how to sync/restore
metadata:
  type: reference
---

- Public (sanitized, no client names, for friends): https://github.com/soumil-garg/static-ad-creatives-maker-by-sg
- Private (client work + Claude context): https://github.com/soumil-garg/bbm-workspace, cloned at C:\cca. Context in `claude-context/`; `sync.ps1` pushes latest, `restore.ps1` sets up a new laptop.
- Vault: https://github.com/soumil-garg/soumil-garg-vault (private)

**Why:** Soumil wants all client work on GitHub and a one-step restore on another laptop. Client work must never go in the public repo.
**How to apply:** After client creative work, run claude-context/sync.ps1. When the skill changes, update the full copy in bbm-workspace AND re-sanitize into the public repo (replace client names with Brand A/B, "Soumil" with "the user"). Ask before pushing, per global rules, unless he has said to sync.
