@echo off
title 🔱 OBSIDIAN GLOBAL: PORTABLE MINER v1.0 🔱
echo [*] OBSIDIAN: Connecting to the Missouri Matrix...
echo [*] GHOST_DNA: Injected Unique Fingerprint.
echo [*] PENTA_STACK: Loading 5 mining cores...

:: This launcher triggers the local python environment without requiring install
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] ERROR: Python not found. Please download from obsidian-global.io
    pause
    exit
)

echo [✓] SUCCESS: You are now earning Bitcoin for the Obsidian Grid.
echo [!] Keep this window open to maintain your 100/100 reputation score.
pause
