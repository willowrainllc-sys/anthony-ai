# --- WILLOW RAIN COMPANY LLC: FULL FLEET LAUNCHER v1.0 ---
import os
import subprocess
import time
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent

FLEET_SCRIPTS = [
    "obsidian_daemon_core.py", # THE WATCHDOG (LAUNCH FIRST)
    "daemon_worker.py",
    "production_worker.py",
    "node_youtube.py",
    "node_facebook.py",
    "node_instagram_threads.py",
    "node_x.py",
    "iptv_signal_harvester.py"
]

def launch_fleet():
    print("[SUPREME] WILLOW RAIN: Initiating Full Fleet Deployment...")

    for script in FLEET_SCRIPTS:
        script_path = BACKEND_DIR / script
        if script_path.exists():
            print(f"Launching {script} in background...")
            # Using Start-Process python to run in background without blocking this script
            cmd = f"powershell.exe -Command \"Start-Process python -ArgumentList '{script_path}' -NoNewWindow\""
            subprocess.run(cmd, shell=True)
            time.sleep(2) # Stagger launches
        else:
            print(f"[-] ERROR: {script} not found at {script_path}")

    print(" FLEET DEPLOYED. All workers active in the background.")

if __name__ == "__main__":
    launch_fleet()
