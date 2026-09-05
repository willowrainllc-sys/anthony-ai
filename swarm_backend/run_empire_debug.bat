@echo off
TITLE EMPIRE DEBUG MODE
cd /d "%~dp0"
echo [*] Killing all python/uvicorn...
taskkill /F /IM python.exe /T
taskkill /F /IM uvicorn.exe /T

echo [*] Starting Mind Server...
start "MIND_SERVER" /min cmd /c "C:\Users\willo\OneDrive\Desktop\Anthony_Ai\venv\Scripts\python.exe -m uvicorn nexus_core:app --host 0.0.0.0 --port 8000 > ..\debug_mind_server.log 2>&1"

echo [*] Starting Quantum Watchdog...
start "QUANTUM_WATCHDOG" /min cmd /c "C:\Users\willo\OneDrive\Desktop\Anthony_Ai\venv\Scripts\python.exe quantum_recovery_node.py > ..\debug_quantum.log 2>&1"

echo [*] EMPIRE RELAUNCHED IN DEBUG MODE.
echo [!] Watch ..\debug_mind_server.log and ..\debug_quantum.log
pause
