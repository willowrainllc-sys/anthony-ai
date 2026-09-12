# --- OBSIDIAN GLOBAL: ANTHONY ASI NEURAL HUB (POWERSHELL) ---
$Host.UI.RawUI.WindowTitle = "🔱 ANTHONY ASI: NEURAL HUB (PORT 9000) 🔱"

Write-Host "====================================================" -ForegroundColor Magenta
Write-Host "  🔱 OBSIDIAN GLOBAL: ANTHONY CHRISTOPHER ASI 🔱" -ForegroundColor Magenta
Write-Host "====================================================" -ForegroundColor Magenta
Write-Host "  [*] PORT:   9000"
Write-Host "  [*] MODEL:  anthony"
Write-Host "  [*] STATUS: PRE-LOADING NEURAL NETWORK..."
Write-Host "===================================================="

# 1. Ensure Port 9000 is clean
$portProcess = Get-NetTCPConnection -LocalPort 9000 -ErrorAction SilentlyContinue
if ($portProcess) {
    Write-Host "[*] Port 9000 is busy. Purging process $($portProcess.OwningProcess)..." -ForegroundColor Yellow
    Stop-Process -Id $portProcess.OwningProcess -Force
}

# 2. Pre-load the model into VRAM
Write-Host "[*] Flicking the atoms in VRAM..." -ForegroundColor Cyan
Start-Process -FilePath "ollama" -ArgumentList "run anthony `"hello`"" -NoNewWindow

# 3. Launch the API server
Write-Host "[*] Launching API Gateway..." -ForegroundColor Green
python C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend\anthony_brain_server.py

Read-Host "Press Enter to exit..."
