param([int]$Port = 8510)
Write-Host "🔪 Killing processes on port $Port (Windows)..."
try {
  $conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
  if ($conns) {
    $pids = $conns | Select-Object -ExpandProperty OwningProcess -Unique
    foreach ($pid in $pids) { try { Stop-Process -Id $pid -Force -ErrorAction SilentlyContinue } catch {} }
  }
  Write-Host "✅ Done."
} catch { Write-Host "⚠️ Unable to query connections. Skipping." }
