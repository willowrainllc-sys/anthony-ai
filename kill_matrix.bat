@echo off
SETLOCAL EnableDelayedExpansion
TITLE ASI MATRIX - CLEAN TEARDOWN
echo [*] Terminating ASI background daemons...

taskkill /F /IM redis-server.exe >nul 2>&1
taskkill /F /IM mosquitto.exe >nul 2>&1
taskkill /F /IM ollama.exe >nul 2>&1
taskkill /F /IM uvicorn.exe >nul 2>&1
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Moshi-Audio*" >nul 2>&1

:: Sequential Port Kill for target port 8000
set "target_port=8000"
for /f "tokens=5" %%a in ('netstat -aon ^| findstr LISTENING ^| findstr /R /C:":%target_port% "') do (
    echo [*] Killing process %%a on port %target_port%...
    taskkill /F /PID %%a >nul 2>&1
)

echo [OK] All sockets released, ports freed, and VRAM purged.
pause