param([string]$SaveKey, [string]$SaveId, [string]$Next, [string]$Dir = 'p4', [string]$Json = 'chats_v4.json')
$f = "C:\cca\habbits\$Json"
if (-not (Test-Path $f)) { '{}' | Set-Content -Encoding utf8 $f }
if ($SaveKey) {
  $j = Get-Content $f -Raw | ConvertFrom-Json
  $j | Add-Member -NotePropertyName $SaveKey -NotePropertyValue $SaveId -Force
  $j | ConvertTo-Json | Set-Content -Encoding utf8 $f
}
if ($Next) { Set-Clipboard -Value (Get-Content -Raw -Encoding UTF8 "C:\cca\habbits\$Dir\$Next.txt") }
