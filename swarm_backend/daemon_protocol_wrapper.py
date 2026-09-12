# --- WILLOW RAIN COMPANY LLC: UNIVERSAL DAEMON PROTOCOL WRAPPER v1.0 ---
import asyncio
import sys
import time
import subprocess
import os
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

class DaemonProtocol:
    """
    UNIVERSAL DAEMON PROTOCOL:
    Turns any Python script into a persistent, self-healing background daemon.
    1. PERSISTENCE: Guarantees the script runs forever.
    2. RECOVERY: Automatically restarts on exit or crash.
    3. INTEGRITY: Logs heartbeats to the Obsidian Central Brain.
    """
    def __init__(self, script_name: str, interval_sec: int = 30):
        self.script_name = script_name
        self.interval = interval_sec
        self.backend_dir = Path(__file__).resolve().parent

    async def run_forever(self):
        swarm_log(f"DAEMON_PROTOCOL: Establishing permanent life-support for [{self.script_name}]", node="DAEMON")

        while True:
            try:
                if not self._is_running():
                    swarm_log(f"[-] DAEMON_PROTOCOL: [{self.script_name}] is offline. Re-igniting...", node="DAEMON")
                    self._start()
                    db.log_event("DAEMON", "BOT_REIGNITED", {"bot": self.script_name})

                # Pulse to signify daemon is watching
                db.log_event("DAEMON", "HEARTBEAT", {"bot": self.script_name})

                await asyncio.sleep(self.interval)
            except Exception as e:
                swarm_log(f" DAEMON_PROTOCOL ERROR: {e}", node="DAEMON")
                await asyncio.sleep(60)

    def _is_running(self):
        try:
            cmd = f'tasklist /FI "IMAGENAME eq python.exe" /V'
            output = subprocess.check_output(cmd, shell=True).decode('utf-8', errors='ignore')
            return self.script_name in output
        except:
            return False

    def _start(self):
        script_path = self.backend_dir / self.script_name
        cmd = f"powershell.exe -Command \"Start-Process python -ArgumentList '{script_path}' -NoNewWindow\""
        subprocess.run(cmd, shell=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        daemon = DaemonProtocol(target)
        asyncio.run(daemon.run_forever())
    else:
        print("Usage: python daemon_protocol_wrapper.py <script_name.py>")
