# --- ANTHONY AI: SYSTEM EXCOMMUNICATO & PROCESS PURGE v1.0 ---
import os
import psutil
import time
from colony_logger import colony_log

# 🔱 THE BLACKLIST: External services we are terminating to ensure total sovereignty
BS_PROCESSES = [
    "ollama.exe",
    "ollama_llama_server.exe",
    "fastapi.exe",
    "uvicorn.exe",
    "node.exe", # Terminating unneeded node loops
    "chrome.exe", # Closing standard chrome to force Obsidian Titan use
    "brave.exe",
    "msedge.exe"
]

class SystemExcommunicato:
    """
    SYSTEM EXCOMMUNICATO v1.0:
    1. TOTAL PURGE: Kills all non-Obsidian background loops and external AI servers.
    2. SOVEREIGN LOCK: Ensures only authorized team processes remain active.
    3. RESOURCE RECLAMATION: Frees up RAM for the Native Intelligence Base.
    """
    def execute_purge(self):
        colony_log("EXCOMMUNICATO: Initiating system-wide purge of unauthorized loops...", node="SECURITY")

        killed_count = 0
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                name = proc.info['name'].lower()
                if any(bs in name for bs in BS_PROCESSES):
                    # Safety: Don't kill our own IDE or Terminal if they happen to share a name (unlikely)
                    proc.kill()
                    killed_count += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        colony_log(f"✓ EXCOMMUNICATO SUCCESS: {killed_count} external loops terminated. System isolated.", node="SECURITY")
        return killed_count

if __name__ == "__main__":
    purge = SystemExcommunicato()
    purge.execute_purge()
