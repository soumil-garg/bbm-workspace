# Run on a new laptop after: git clone <this repo> C:\cca
# Restores global CLAUDE.md, commands, custom skills, and auto-memory for the Sessions project.
param([string]$SessionsDir = (Join-Path $HOME "OneDrive\Desktop\CLAUDE\Sessions"))
$here = $PSScriptRoot
$claude = Join-Path $HOME ".claude"
New-Item -ItemType Directory -Force "$claude\skills","$claude\commands" | Out-Null
Copy-Item "$here\CLAUDE.md" "$claude\CLAUDE.md" -Force
Copy-Item "$here\commands\*" "$claude\commands\" -Force
Copy-Item "$here\skills\*" "$claude\skills\" -Recurse -Force
New-Item -ItemType Directory -Force $SessionsDir | Out-Null
# Claude Code names the project folder by replacing : \ / with '-' in the path
$slug = ($SessionsDir -replace '[:\/]', '-')
$memDir = Join-Path $claude "projects\$slug\memory"
New-Item -ItemType Directory -Force $memDir | Out-Null
Copy-Item "$here\memory\*" $memDir -Force
Write-Host "Restored. Memory at $memDir. Open Claude Code in $SessionsDir."
Write-Host "Still manual: APIFY_TOKEN env var, PostHog OAuth, Meta/Arcads/Higgsfield connectors, Vault clone, third-party repos (see third-party-repos.txt)."
