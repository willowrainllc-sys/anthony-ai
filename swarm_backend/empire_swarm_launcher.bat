@echo off
title EMPIRE SWARM COMMANDER
echo 🔱 INITIALIZING EMPIRE SWARM...
cd /d "C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend"

:: Start Mind Server
echo [*] Launching Empire Mind Server...
start "Empire Mind Server" cmd /k "title Empire Mind Server && C:\Users\willo\OneDrive\Desktop\Anthony_Ai\venv\Scripts\python.exe -m uvicorn nexus_core:app --host 127.0.0.1 --port 8000"

:: Wait for server boot
timeout /t 5

:: Start Pipeline
echo [*] Launching Video Swarm Pipeline...
start "Video Swarm Pipeline" cmd /k "title Video Swarm Pipeline && C:\Users\willo\OneDrive\Desktop\Anthony_Ai\venv\Scripts\python.exe master_pipeline.py"

echo 🔱 SWARM ACTIVE. Watch the windows above.
pause
