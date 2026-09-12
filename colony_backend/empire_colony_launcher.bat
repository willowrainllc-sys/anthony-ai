@echo off
title EMPIRE COLONY COMMANDER
echo 🔱 INITIALIZING EMPIRE COLONY...
cd /d "C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\colony_backend"

:: Start Mind Server
echo [*] Launching Empire Mind Server...
start "Empire Mind Server" cmd /k "title Empire Mind Server && C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\venv\Scripts\python.exe -m uvicorn nexus_core:app --host 127.0.0.1 --port 8000"

:: Wait for server boot
timeout /t 5

:: Start Pipeline
echo [*] Launching Video Colony Pipeline...
start "Video Colony Pipeline" cmd /k "title Video Colony Pipeline && C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\venv\Scripts\python.exe master_pipeline.py"

echo 🔱 COLONY ACTIVE. Watch the windows above.
pause
