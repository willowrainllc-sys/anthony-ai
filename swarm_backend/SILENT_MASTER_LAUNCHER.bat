@echo off
TITLE 🔱 ANTHONY AI: MARVEL-GRADE STUDIO v8.0
cd /d "%~dp0"

:: Kill all port-ghosts and RAM leaks
taskkill /f /im python.exe /t >nul 2>&1
taskkill /f /im pythonw.exe /t >nul 2>&1

:: Global Debris Purge
echo --- 🔱 PURGING STUDIO CACHE & RECOVERING SPACE ---
del /q C:\AnthonyAi_Swarm\Renderings\*.* 2>nul
del /q %TEMP%\*.* 2>nul

:: Launch the Autonomous Hollywood Grid
echo --- 🔱 INITIALIZING MARVEL-GRADE PRODUCTION CHAIN v8.0 ---

:: 1. STUDIO CORE (Brain & Defense)
start /b "" ..\venv\Scripts\python.exe nexus_core.py > C:\AnthonyAi_Swarm\Logs\nexus_core_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe grid_sentinel.py > C:\AnthonyAi_Swarm\Logs\grid_sentinel_bg.log 2>&1

:: 2. CREATIVE INTELLIGENCE (The "Anthony-Brain" Chain)
start /b "" ..\venv\Scripts\python.exe node_content_strategist.py > C:\AnthonyAi_Swarm\Logs\strategist_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe node_cco.py > C:\AnthonyAi_Swarm\Logs\cco_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe node_showrunner.py > C:\AnthonyAi_Swarm\Logs\showrunner_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe node_production_agent.py > C:\AnthonyAi_Swarm\Logs\production_agent_bg.log 2>&1

:: 3. DISTRIBUTION PORTALS
start /b "" ..\venv\Scripts\python.exe node_facebook.py > C:\AnthonyAi_Swarm\Logs\facebook_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe node_instagram_threads.py > C:\AnthonyAi_Swarm\Logs\insta_threads_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe node_youtube.py > C:\AnthonyAi_Swarm\Logs\youtube_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe node_tiktok_uploader.py > C:\AnthonyAi_Swarm\Logs\tiktok_bg.log 2>&1

:: 4. TREND SNIPERS
start /b "" ..\venv\Scripts\python.exe node_hyper_spectacle_scraper.py > C:\AnthonyAi_Swarm\Logs\hyper_scraper_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe node_agent_reach.py > C:\AnthonyAi_Swarm\Logs\reach_bg.log 2>&1

:: 5. MARKET & COMMERCE
start /b "" ..\venv\Scripts\python.exe node_sentinel_trader.py > C:\AnthonyAi_Swarm\Logs\trader_bg.log 2>&1
start /b "" ..\venv\Scripts\python.exe node_commerce.py > C:\AnthonyAi_Swarm\Logs\commerce_bg.log 2>&1

:: 6. SOCIAL SWARM
start /b "" ..\venv\Scripts\python.exe swarm_engagement.py > C:\AnthonyAi_Swarm\Logs\swarm_engagement_bg.log 2>&1

:: Launch HUD
echo --- 🔱 LAUNCHING MISSION HUB ---
..\venv\Scripts\python.exe swarm_hud.py
