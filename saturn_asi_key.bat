@echo off
title 🔱 SATURN ASI: THE MASTER KEY 🔱
color 0D

echo ====================================================
echo   🔱 SATURN GLOBAL: ARTIFICIAL SUPER INTELLIGENCE 🔱
echo ====================================================
echo   [!] IDENTITY: Anthony Christopher Maestas (ASI-01)
echo   [!] STATUS:   ARMING THE MASTER KEY...
echo ====================================================

cd /d "%~dp0"

:: 1. Verify / Install Core Environment
echo [*] PHASE 1: Synchronizing Nervous System (Ollama)...
where ollama >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: ASI require Ollama. Please install from ollama.com
    pause
    exit
)

:: 2. Load the ASI Brain
echo [*] PHASE 2: Loading Supreme ASI Intelligence...
anthony-engine list | findstr "Anthony-Christopher-Maestas" >nul
if %errorlevel% neq 0 (
    echo [!] Creating Brain v13.0 (ASI Edition)...
    anthony-engine create Anthony-Christopher-Maestas -f swarm_backend/Modelfile_Anthony_Christopher.0
)

:: 3. Ignite the Private API (Port 9000)
echo [*] PHASE 3: Opening Private Brain Port (9000)...
start /b python swarm_backend/saturn_brain_server.py

:: 4. Ignite the Sovereign Matrix (101 Ports)
echo [*] PHASE 4: Opening the 1,001 Port Matrix...
start /b python swarm_backend/saturn_pproxy_runner.py

:: 5. Launch the Persistence Kernel (Stay Attacking)
echo [*] PHASE 5: Locking the Immortality Kernel...
start /b python swarm_backend/saturn_command_os.py

echo ====================================================
echo   🔱 SUCCESS: THE MASTER KEY IS ACTIVE. 🔱
echo   [!] All terminals decoupled and routing.
echo   [!] Saturn Global is mining for the Director.
echo ====================================================
timeout /t 5
exit
