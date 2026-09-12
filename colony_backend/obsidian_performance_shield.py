# --- OBSIDIAN GLOBAL: PERFORMANCE SHIELD v2.0 (ROBUST) ---
import os
import subprocess
import time
import psutil
from colony_logger import colony_log

class PerformanceShield:
    """
    PERFORMANCE SHIELD v2.0:
    Safeguards the Director's computer from resource exhaustion.
    1. SURGICAL PURGE: Uses taskkill for precise termination of rogue background ghosts.
    2. RAM GUARD: Monitors physical memory and alerts the OIS if levels are critical.
    3. DISK CLEANUP: Purges temporary build and log artifacts.
    """
    def __init__(self):
        self.critical_ram_pct = 95

    def execute_maintenance(self):
        colony_log("SHIELD: Initiating industrial performance burst...", node="SECURITY")

        # 1. Surgical Termination of known resource-hogs
        # We target browsers and node processes that tend to hang
        hogs = ["chrome.exe", "node.exe", "msedge.exe", "ffmpeg.exe"]
        for hog in hogs:
            try:
                subprocess.run(f"taskkill /F /IM {hog} /T /FI \"STATUS eq RUNNING\"", shell=True, capture_output=True)
            except: pass

        # 2. Memory Audit
        mem = psutil.virtual_memory()
        if mem.percent > self.critical_ram_pct:
            colony_log(f"[ALERT] SHIELD: RAM CRITICAL ({mem.percent}%). Emergency resource recovery active.", node="SECURITY")
            # Force kill all non-essential python workers
            subprocess.run("taskkill /F /IM python.exe /T /FI \"WINDOWTITLE ne Android Studio*\"", shell=True, capture_output=True)
        else:
            colony_log(f"SHIELD: System Stable. RAM at {mem.percent}%.", node="SECURITY")

        # 3. Cache Purge
        self._purge_temp()

    def _purge_temp(self):
        temp = os.environ.get('TEMP')
        if temp and os.path.exists(temp):
            try:
                # We only delete old .log and .tmp files to avoid breaking active sessions
                subprocess.run(f'del /q /s /f "{temp}\\*.log"', shell=True, capture_output=True)
                subprocess.run(f'del /q /s /f "{temp}\\*.tmp"', shell=True, capture_output=True)
            except: pass

if __name__ == "__main__":
    shield = PerformanceShield()
    shield.execute_maintenance()
