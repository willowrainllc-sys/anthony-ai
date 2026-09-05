@echo off
TITLE Empire Mind Server [STABLE]
COLOR 0A

echo ============================================================
echo  EMPIRE MIND SERVER: INITIALIZING...
echo ============================================================

cd /d "C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend"

"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\venv\Scripts\python.exe" -m uvicorn nexus_core:app --host 127.0.0.1 --port 8000 --reload

echo [!] Mind Server exited.
pause
