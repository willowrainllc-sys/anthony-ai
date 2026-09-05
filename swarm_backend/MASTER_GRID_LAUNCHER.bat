@echo off
TITLE 🔱 EMPIRE SWARM: MASTER GRID LAUNCHER
cd /d "%~dp0"

echo --- 🔱 INITIALIZING ALPHA SPECTRUM NODES ---

:: 1. Mind Server (Nexus Core)
start "🧠 NEXUS CORE: MIND SERVER" cmd /k "..\venv\Scripts\python.exe nexus_core.py"

:: 2. Frontend Dispatcher (Physical Phone Posting)
start "📲 FRONTEND DISPATCHER: PHONE POSTING" cmd /k "..\venv\Scripts\python.exe execute_live_strikes.py"

:: 3. Disciples Autopilot (Bot Browsing/Liking)
start "👥 DISCIPLES AUTOPILOT: BOT GRID" cmd /k "..\venv\Scripts\python.exe run_disciples_autopilot.py"

:: 4. Heavy Engagement (Phone Socializing)
start "🔥 MOBILE HEAVY ENGAGEMENT" cmd /k "..\venv\Scripts\python.exe mobile_heavy_engagement.py"

:: 5. Social Engagement (Auto-Reply API)
start "💬 SOCIAL ENGAGEMENT: AUTO-REPLIES" cmd /k "..\venv\Scripts\python.exe node_engagement.py"

:: 6. Ghost Status Striker (Text Posts)
echo [*] Ghost Status Striker will run in a separate loop for text updates.
start "🔱 GHOST FRONTEND: STATUS STRIKES" cmd /k "..\venv\Scripts\python.exe ghost_frontend_status_post.py"

echo.
echo ====================================================
echo   🔱 GRID FULLY SYNCHRONIZED
echo   Check separate windows for real-time logs.
echo ====================================================
pause
