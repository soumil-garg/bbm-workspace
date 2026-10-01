# BBM Workspace (PRIVATE)

Big Bigger Media client creative work plus the Claude context needed to continue on any laptop.
Client work and context. Private memory files (mentorship, unit economics, account watch, ChatGPT login notes) are deliberately excluded from this repo; they stay local. The public skill lives at
https://github.com/soumil-garg/static-ad-creatives-maker-by-sg (sanitized, no client names).

## Layout
- `savvy/ habbits/ mufasa/ ashopi/` per-client prompts, generated creatives, research, chat logs
- `claude-context/` CLAUDE.md, memory (client contexts, feedback, references), commands, custom skills (full, un-sanitized)
- `claude-context/third-party-repos.txt` cloned tools that are gitignored here

## New laptop
```powershell
git clone https://github.com/soumil-garg/bbm-workspace.git C:\cca
powershell -ExecutionPolicy Bypass -File C:\cca\claude-context\restore.ps1
```
Then open Claude Code in `Desktop\CLAUDE\Sessions`. Memory loads automatically. Then do the manual items restore.ps1 lists.

## Keeping it current
After a work session: `powershell -File C:\cca\claude-context\sync.ps1`
Rule: every client deliverable goes in `C:\cca\<client>\` and gets synced.
