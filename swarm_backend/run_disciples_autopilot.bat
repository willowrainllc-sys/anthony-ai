@echo off
TITLE EMPIRE DISCIPLES AUTOPILOT
cd /d "%~dp0"
echo --- 🔱 STARTING HUMAN EMULATION GRID ---
..\venv\Scripts\python.exe run_disciples_autopilot.py
pause
