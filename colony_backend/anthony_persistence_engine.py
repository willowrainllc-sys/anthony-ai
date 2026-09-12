# --- OBSIDIAN GLOBAL: PERSISTENCE KERNEL v7.0 (STABLE) ---
import os
import sys
import time
import asyncio
import subprocess
import psutil
from pathlib import Path

# Fix character encoding issues for logs
def log(msg):
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] [SECURITY] {msg}")

class AnthonyChristopherPersistenceEngine:
    """
    STABLE PERSISTENCE KERNEL:
    Monitors core system components without recursive crashing.
    """
    def __init__(self):
        self.critical_scripts = [
            "obsidian_pproxy_runner.py",
            "anthony_daemon_core.py",
            "obsidian_permanent_burst_loop.py",
            "anthony_brain_server.py"
        ]
        self.backend_dir = Path(__file__).resolve().parent

    async def audit_fleet(self):
        # 1. RAM Shield: Don't spawn if RAM > 95%
        mem_pct = psutil.virtual_memory().percent
        if mem_pct > 95:
            log(f"ALERT: RAM CRITICAL ({mem_pct}%). Throttling re-spawn.")
            return

        # 2. Check Process List
        try:
            output = subprocess.check_output('tasklist /FI "IMAGENAME eq python.exe" /V /NH', shell=True).decode('utf-8', errors='ignore')
        except: output = ""

        for script in self.critical_scripts:
            if script not in output:
                log(f"RE-IGNITING: {script}")
                script_path = self.backend_dir / script
                subprocess.Popen(f"start /b python {script_path}", shell=True)
                await asyncio.sleep(5) # Give time to settle

    async def run_loop(self):
        log("PERSISTENCE KERNEL v7.0 ACTIVE.")
        while True:
            try:
                await self.audit_fleet()
                await asyncio.sleep(300) # 5-minute pulse
            except Exception as e:
                log(f"ERROR: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    engine = AnthonyChristopherPersistenceEngine()
    asyncio.run(engine.run_loop())
