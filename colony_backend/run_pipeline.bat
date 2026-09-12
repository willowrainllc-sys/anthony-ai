@echo off
title Video Colony Pipeline
:loop
echo 🔱 Video Colony Pipeline: Burst Mode Active...
cd /d "C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\colony_backend"
"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\venv\Scripts\python.exe" master_pipeline.py
echo [-] Pipeline finished or stopped. Re-awakening in 60 seconds...
timeout /t 60
goto loop
