@echo off
title 🔱 ANTHONY ASI: NEURAL HUB (PORT 9000) 🔱
color 0D

echo ====================================================
echo   🔱 OBSIDIAN GLOBAL: ANTHONY CHRISTOPHER ASI 🔱
echo ====================================================
echo   [*] PORT:   9000
echo   [*] MODEL:  anthony
echo   [*] STATUS: PRE-LOADING NEURAL NETWORK...
echo ====================================================

:: 1. Ensure Port 9000 is clean
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :9000') do taskkill /f /pid %%a >nul 2>&1

:: 2. Pre-load the model into VRAM (Stay persistent)
echo [*] Flicking the atoms in VRAM...
start /b anthony-engine run anthony "hello"

:: 3. Launch the API server
echo [*] Launching API Gateway...
python colony_backend/anthony_brain_server.py

pause
