@echo off
SETLOCAL EnableDelayedExpansion
TITLE Maga Media Empire - High Performance Swarm
COLOR 0E

echo ============================================================
echo  MAGA MEDIA EMPIRE: HIGH-PERFORMANCE SWARM UPGRADE
echo ============================================================

:: 1. Check for Admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] ERROR: Please run this script as ADMINISTRATOR.
    pause
    exit /b 1
)

:: 2. Identify Current IP
echo [*] Detecting Local Identity...
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4 Address" ^| findstr /C:"192.168."') do (
    set "RAW_IP=%%a"
    set "WIFI_IP=!RAW_IP: =!"
)
echo [WIFI] Current IP: %WIFI_IP%

:: 3. Clear and Reset Firewall Rules
echo [*] Resetting Swarm Firewall Gates...
powershell -Command "Remove-NetFirewallRule -DisplayName 'Swarm Brain' -ErrorAction SilentlyContinue"
powershell -Command "Remove-NetFirewallRule -DisplayName 'Swarm n8n' -ErrorAction SilentlyContinue"
powershell -Command "New-NetFirewallRule -DisplayName 'Swarm Brain' -Direction Inbound -LocalPort 8000,11434 -Protocol TCP -Action Allow -Profile Private,Public"
powershell -Command "New-NetFirewallRule -DisplayName 'Swarm n8n' -Direction Inbound -LocalPort 5678 -Protocol TCP -Action Allow -Profile Private,Public"
echo [OK] Firewall gates 8000, 5678, and 11434 are now wide open.

:: 4. Force Port 8000 and 11434 Cleanup
echo [*] Cleaning Ghost Handshakes...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :11434 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

:: 5. Restart Infrastructure (FORCED GPU MODE)
echo [*] Launching Ollama Core with Hardware Acceleration...
taskkill /F /IM ollama.exe >nul 2>&1
set OLLAMA_NUM_PARALLEL=1
set OLLAMA_GPU_OVERHEAD=0
start "Ollama-Core" cmd /c "ollama serve"

timeout /t 5 /nobreak >nul

:: 6. Trigger TMZ Scraper for Fresh Intel
echo [*] Triggering TMZ Scraper...
set "BACKEND_DIR=%~dp0swarm_backend"
if exist "!BACKEND_DIR!\scrape_tmz.py" (
    cd /d "!BACKEND_DIR!"
    python scrape_tmz.py
) else (
    echo [!] WARNING: TMZ Scraper not found at !BACKEND_DIR!\scrape_tmz.py
)

:: 7. Launch Mind Server on all interfaces
echo [*] Booting Mind Server (0.0.0.0 Binding)...
if exist "!BACKEND_DIR!" (
    cd /d "!BACKEND_DIR!"
    start "Mind-Server" cmd /c "python -m uvicorn nexus_core:app --host 0.0.0.0 --port 8000 --reload"
) else (
    echo [!] ERROR: Swarm backend directory missing at !BACKEND_DIR!
)

echo ------------------------------------------------------------
echo  MAGA MEDIA EMPIRE UPGRADE COMPLETE
echo  1. GPU ACCELERATION: ACTIVE (OLLAMA_NUM_GPU=1)
echo  2. TMZ INTEL: SCRAPED AND STORED
echo  3. NETWORK: OPTIMIZED FOR WI-FI
echo ------------------------------------------------------------
pause
