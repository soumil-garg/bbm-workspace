# Records ChatGPT chat IDs and puts the next prompt on the clipboard.
# Usage: & chatgpt_helper.ps1 -Work C:\cca\brand -Dir p -Json chats.json -SaveKey C1_M_Name -SaveId <chat uuid> -Next C1_P_Name
param(
  [string]$Work = 'C:\cca\brand',
  [string]$Dir = 'p',
  [string]$Json = 'chats.json',
  [string]$SaveKey,
  [string]$SaveId,
  [string]$Next
)
$f = Join-Path $Work $Json
if (-not (Test-Path $f)) { '{}' | Set-Content -Encoding utf8 $f }
if ($SaveKey) {
  $j = Get-Content $f -Raw | ConvertFrom-Json
  $j | Add-Member -NotePropertyName $SaveKey -NotePropertyValue $SaveId -Force
  $j | ConvertTo-Json | Set-Content -Encoding utf8 $f
}
if ($Next) { Set-Clipboard -Value (Get-Content -Raw -Encoding UTF8 (Join-Path (Join-Path $Work $Dir) "$Next.txt")) }
