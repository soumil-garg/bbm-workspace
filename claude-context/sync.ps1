# Run on the laptop where you worked: pulls latest context from ~/.claude into this repo, commits, pushes.
$here = $PSScriptRoot
$claude = Join-Path $HOME ".claude"
$sessions = Join-Path $HOME "OneDrive\Desktop\CLAUDE\Sessions"
$slug = ($sessions -replace '[:\/]', '-')
Copy-Item "$claude\projects\$slug\memory\*" "$here\memory\" -Force
Get-ChildItem "$here\memory\*.md" | ForEach-Object { (Get-Content $_ -Raw) -replace 'phx_[A-Za-z0-9]{20,}','[REDACTED]' | Set-Content $_ -NoNewline }
Copy-Item "$claude\CLAUDE.md" "$here\CLAUDE.md" -Force
Copy-Item "$claude\commands\*" "$here\commands\" -Force
foreach ($s in "static-ad-creatives-maker-by-sg","brief","daily","weekly") { Copy-Item "$claude\skills\$s\*" "$here\skills\$s\" -Recurse -Force }
Set-Location (Split-Path $here -Parent)
git add -A; git commit -m "Sync $(Get-Date -Format yyyy-MM-dd)"; git push
