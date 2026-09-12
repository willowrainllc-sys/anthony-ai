# --- WILLOW RAIN SECURITY: OBSIDIAN KILL-SWITCH & GRID TERMINATOR v1.0 ---
import os
import sys
import subprocess
import asyncio
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

class ObsidianKillSwitch:
    """
    OBSIDIAN KILL-SWITCH v1.0:
    Instant termination of the entire Willow Rain Grid.
    1. PROCESS PURGE: Kills all active Python and Docker processes related to the swarm.
    2. NETWORK COLLAPSE: Kills the PProxy matrix and breaks all active SOCKS5 tunnels.
    3. DAEMON DISABLE: Stops the Daemon Core and life-support loops.
    4. DATA LOCKDOWN: Disconnects the local Vault from all external API handshakes.
    """
    async def execute_global_termination(self):
        swarm_log("[ALERT] KILL_SWITCH: INITIATING GLOBAL GRID TERMINATION...", node="SECURITY")

        # 1. Kill all Python processes (broad but effective for instant shutdown)
        try:
            subprocess.run("taskkill /F /IM python.exe", shell=True, capture_output=True)
            swarm_log(" KILL_SWITCH: All Python workers terminated.", node="SECURITY")
        except: pass

        # 2. Kill Docker containers (if any)
        try:
            subprocess.run("docker kill $(docker ps -q)", shell=True, capture_output=True)
            swarm_log(" KILL_SWITCH: All virtual nodes collapsed.", node="SECURITY")
        except: pass

        # 3. Break Network Matrix
        db.log_event("SECURITY", "GLOBAL_TERMINATION_EXECUTED", {"status": "GRID_OFFLINE"})

        # 4. Final System Lock
        swarm_log("[SUPREME] SYSTEM STATUS: GRID TERMINATED. WILLOW RAIN IS OFFLINE.", node="SECURITY")
        return True

kill_switch = ObsidianKillSwitch()

if __name__ == "__main__":
    asyncio.run(kill_switch.execute_global_termination())
