# --- WILLOW RAIN: FLEET RESTART SCRIPT ---
Stop-Process -Name python -ErrorAction SilentlyContinue

Write-Host "🔱 Restarting Willow Rain Fleet..." -ForegroundColor Cyan

$scripts = @(
    "daemon_worker.py",
    "production_worker.py",
    "node_youtube.py",
    "node_facebook.py",
    "node_instagram_threads.py",
    "node_x.py",
    "iptv_signal_harvester.py"
)

foreach ($s in $scripts) {
    Write-Host "Launching $s..."
    Start-Process python -ArgumentList "swarm_backend/$s" -NoNewWindow
    Start-Sleep -Seconds 3
}

Write-Host "✓ Fleet Online." -ForegroundColor Green
