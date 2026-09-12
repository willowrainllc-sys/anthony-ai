@echo off
taskkill /f /im python.exe
timeout /t 2
start /b python swarm_backend/sovereign_daemon_core.py
timeout /t 2
start /b python swarm_backend/sovereign_pproxy_runner.py
timeout /t 2
start /b python swarm_backend/honey_comb_daemon.py
timeout /t 2
start /b python swarm_backend/daemon_worker.py
timeout /t 2
start /b python swarm_backend/production_worker.py
timeout /t 2
start /b python swarm_backend/node_youtube.py
timeout /t 2
start /b python swarm_backend/node_facebook.py
timeout /t 2
start /b python swarm_backend/node_instagram_threads.py
timeout /t 2
start /b python swarm_backend/node_x.py
timeout /t 2
start /b python swarm_backend/iptv_signal_harvester.py
echo 🔱 Sovereign Fleet v9.1 Launched. Honey Comb Feeding Active.
