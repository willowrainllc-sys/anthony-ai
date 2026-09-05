@echo off
title Video Swarm Pipeline
:loop
echo 🔱 Video Swarm Pipeline: Strike Mode Active...
cd /d "C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend"
"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\venv\Scripts\python.exe" master_pipeline.py
echo [-] Pipeline finished or stopped. Re-awakening in 60 seconds...
timeout /t 60
goto loop
