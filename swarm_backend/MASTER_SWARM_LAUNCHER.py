# --- ANTHONY AI: MASTER SOVEREIGN ORCHESTRATOR v1.7 (EMPIRE & GROWTH) ---
import subprocess
import sys
import os
import time
import signal
from pathlib import Path

# Force UTF-8
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = Path(__file__).resolve().parent
PYTHON_EXE = sys.executable

NODES = [
    {"name": "MIND_SERVER", "script": "nexus_core.py"},
    {"name": "STRIKE_WORKER", "script": "execute_live_strikes.py"},
    {"name": "DIRECTOR_ENGINE", "script": "anthony_video_publisher.py"},
    {"name": "PRODUCTION_WORKER", "script": "production_worker.py"},
    {"name": "ANALYTICS_RADAR", "script": "analytics_node.py"},
    {"name": "OSINT_WATCHDOG", "script": "node_osint_watchdog.py"},
    {"name": "TACTICAL_MONITOR", "script": "node_tactical_monitor.py"},
    {"name": "REVENUE_SYNC", "script": "revenue_sync.py"},
    {"name": "GROWTH_ENGINE", "script": "disciple_growth_engine.py"},
    {"name": "ENGAGEMENT_SWARM", "script": "swarm_engagement.py"},
    {"name": "TIKTOK_STRIKE", "script": "node_tiktok_uploader.py"},
    {"name": "SWARM_HUD", "script": "swarm_hud.py"}
]

processes = {}

def cleanup(signum, frame):
    print("\n[!] SHUTDOWN SIGNAL RECEIVED. TERMINATING EMPIRE GRID...")
    for name, p in processes.items():
        print(f"[-] Stopping {name}...")
        p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)
signal.signal(signal.SIGTERM, cleanup)

def run_swarm():
    print("="*60)
    print("  ANTHONY AI // SOVEREIGN EMPIRE MASTER LAUNCHER v1.7")
    print(f"  LOCATION: {BASE_DIR.drive} (PORTABLE MODE)")
    print("="*60)

    os.environ["MASTER_LAUNCHER"] = "1"

    for node in NODES:
        script_path = BASE_DIR / node['script']
        print(f"[+] Launching {node['name']}...")

        p = subprocess.Popen(
            [PYTHON_EXE, str(script_path)],
            cwd=str(BASE_DIR),
            stdout=None,
            stderr=subprocess.STDOUT,
            env=os.environ.copy()
        )
        processes[node['name']] = p
        time.sleep(2.5)

    print("\n[🚀] ALL NODES OPERATIONAL. EMPIRE IS LIVE.")
    print("[!] Monitor your Pixel 10 for revenue vitals and global drops.")
    print("[!] OSINT Watchdog, Tactical Monitor, Revenue Sync & Growth Engine active.")
    print("[!] Press CTRL+C to terminate.\n")

    while True:
        try:
            for name, p in list(processes.items()):
                poll = p.poll()
                if poll is not None:
                    print(f"\n[!] CRITICAL: Node {name} died (Exit Code: {poll}). Restarting...")
                    script_path = next(n['script'] for n in NODES if n['name'] == name)
                    new_p = subprocess.Popen(
                        [PYTHON_EXE, str(BASE_DIR / script_path)],
                        cwd=str(BASE_DIR),
                        stdout=None,
                        stderr=subprocess.STDOUT,
                        env=os.environ.copy()
                    )
                    processes[name] = new_p
            time.sleep(15)
        except Exception as e:
            print(f"[-] Launcher Loop Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    run_swarm()
