@echo off
SETLOCAL EnableDelayedExpansion
TITLE Anthony AI - Master Swarm Launcher
COLOR 0A

echo ==========================================
echo LAUNCHING ANTHONY AI LOCAL SWARM PIPELINE
echo ==========================================

:: 0. Check for Administrator privileges (Required for Firewall/Port Cleanup)
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] ERROR: Please run this script as ADMINISTRATOR.
    pause
    exit /b 1
)

:: Swarm Performance & VRAM Config
set "OLLAMA_NUM_PARALLEL=1"
set "OLLAMA_MAX_LOADED_MODELS=1"
set "OLLAMA_HOST=127.0.0.1"
set "OLLAMA_IGPU_ENABLE=0"
set "OLLAMA_NUM_GPU=0"

:: 1. Open Firewall Gates (Regular Wi-Fi Optimization)
echo [*] Opening Firewall Gates (8000, 5678, 11434)...
powershell -Command "New-NetFirewallRule -DisplayName 'Swarm Brain' -Direction Inbound -LocalPort 8000,11434 -Protocol TCP -Action Allow -Profile Private,Public -ErrorAction SilentlyContinue" >nul 2>&1
powershell -Command "New-NetFirewallRule -DisplayName 'Swarm n8n' -Direction Inbound -LocalPort 5678 -Protocol TCP -Action Allow -Profile Private,Public -ErrorAction SilentlyContinue" >nul 2>&1

:: 2. Pre-Flight Port Clean
echo [*] Releasing Handshake Ports and Processes...
taskkill /F /IM redis-server.exe >nul 2>&1
taskkill /F /IM mosquitto.exe >nul 2>&1
taskkill /F /IM ollama.exe >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000 ^| findstr LISTENING') do taskkill /F /PID %%a >nul 2>&1

:: 3. Start Infrastructure
echo [*] Launching Redis-Mesh...
start "Redis-Mesh" /min cmd /c "redis-server"

echo [*] Launching Mosquitto-MQTT...
start "Mosquitto-MQTT" /min cmd /c "mosquitto -v"

echo [*] Initializing Ollama-Core (CPU-Stable)...
start "Ollama-Core" cmd /c "set OLLAMA_IGPU_ENABLE=0 && set OLLAMA_NUM_GPU=0 && ollama serve"

:: 4. Launch Master Swarm Core (FastAPI Mind-Server)
timeout /t 5 /nobreak >nul
echo [*] Booting Mind-Server on http://127.0.0.1:8000...
set "BACKEND_DIR=%~dp0swarm_backend"
if exist "!BACKEND_DIR!" (
    start "Mind-Server" cmd /c "cd /d !BACKEND_DIR! && python -m uvicorn nexus_core:app --host 0.0.0.0 --port 8000 --reload"
) else (
    echo [!] ERROR: Swarm backend directory missing at !BACKEND_DIR!
)

:: 5. Spin up n8n and local Docker containers
echo [*] Launching n8n Docker Container...
docker start n8n >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] Docker container 'n8n' not found. Attempting compose up...
    docker compose up -d
)

echo ==========================================
echo ALL SYSTEMS LAUNCHED SUCCESSFULLY!
echo - Ollama:  http://localhost:11434
echo - FastAPI: http://localhost:8000
echo - n8n UI:  http://localhost:5678
echo ==========================================
echo NOTE: Use http://host.docker.internal:8000 inside n8n.
echo ==========================================
pause
