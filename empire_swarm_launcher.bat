@echo off
SETLOCAL EnableDelayedExpansion
TITLE MAGA MEDIA EMPIRE - MISSION SPECTRUM COMMAND (v10006.0)
COLOR 0E

echo ============================================================
echo  MAGA MEDIA EMPIRE: THE FINAL MISSION SPECTRUM (v10006.0)
echo  SYNCHRONIZATION: EVIDENCE-LEAD GRID 4.0
echo  PRESIDENT: ANTHONY MAESTAS
echo ============================================================

:: 1. Admin Check
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [!] ERROR: Please run as ADMINISTRATOR.
    pause
    exit /b 1
)

:: 2. System Synchronization & Purification
echo [*] System Synchronization: Evidence-Lead Grid 4.0...
powershell -Command "Start-Process taskkill -ArgumentList '/F', '/IM', 'python.exe', '/T' -Verb RunAs -Wait" >nul 2>&1

echo [*] Engaging Swarm Purifier...
"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\venv\Scripts\python.exe" "C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend\swarm_purifier.py"

set "VENV_PYTHON=C:\Users\willo\OneDrive\Desktop\Anthony_Ai\venv\Scripts\python.exe"
set "WATCHDOG=C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend\swarm_watchdog.py"

:: 3. AWAKEN THE SPECTRUM GRID
echo [*] Launching THE FINAL MISSION SPECTRUM (v10006.0)...
echo [*] Engaging the Focused Meta-Core Watchdog...
"%VENV_PYTHON%" "%WATCHDOG%"

echo ============================================================
echo  EMPIRE v10006.0 DEPLOYED: MISSION SPECTRUM ACTIVE
echo  - GRID: 4.0 SYNCHRONIZED
echo  - AUTOPILOT: ENGAGED
echo ============================================================
pause
