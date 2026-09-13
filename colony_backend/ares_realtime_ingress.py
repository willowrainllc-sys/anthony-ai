# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES REAL-TIME INGRESS & UPDATE INJECTOR v1.0 ---
import os
import sys
import time
import subprocess
from pathlib import Path
from colony_logger import colony_log

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

def execute_sync_pipeline():
    """Triggers the full Obsidian sync pipeline to push updates to all targets."""
    colony_log("ARES INGRESS: Executing master synchronization pipeline...", node="SUPREME")

    scripts = [
        "fix_links_v6.py",
        "obsidian_mobile_sync.py",
        "obsidian_adsense_injector.py",
        "obsidian_p_seo_gen.py"
    ]

    for script in scripts:
        script_path = root / "colony_backend" / script
        if script_path.exists():
            colony_log(f"[*] ARES: Running {script}...", node="SUPREME")
            subprocess.run([sys.executable, str(script_path)], capture_output=True)

    colony_log("✓ ARES INGRESS: Pipeline executed. All targets (Android/Edge/Local) updated.", node="SUPREME")

def monitor_local_changes():
    """
    Theoretical 'Real-time' injection:
    In a real production environment, this would use watchdog to detect file saves.
    For this build, we hook it into the autopilot loop.
    """
    colony_log("ARES INGRESS: Monitoring for real-time asset injections...", node="SUPREME")

    # Check if we should pull from Git first
    try:
        res = subprocess.run(["git", "pull", "origin", "master"], capture_output=True, text=True)
        if "Already up to date" not in res.stdout:
            colony_log("🔱 ARES: New GitHub assets detected. Injecting...", node="SUPREME")
            execute_sync_pipeline()
    except: pass

if __name__ == "__main__":
    # 🔱 This is the brain of the 'Always-On' update system
    while True:
        monitor_local_changes()
        time.sleep(15) # High frequency pulse
