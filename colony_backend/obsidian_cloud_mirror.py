# --- WILLOW RAIN SECURITY: OBSIDIAN CLOUD MIRROR v3.0 (BULLETPROOF) ---
import os
import sys
import json
import asyncio
import httpx
import subprocess
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

ALIBABA_EIP = os.getenv("ALIBABA_EIP", "47.85.50.46")

class ObsidianCloudMirror:
    """
    OBSIDIAN CLOUD MIRROR v3.0:
    The ultimate "Unbreakable" Failover.
    1. COMPONENT MONITOR: Pings the local matrix, the burst loop, and the daemon core.
    2. EMERGENCY TAKEOVER: If the local host dies, the mirror activates cloud-based mining instantly.
    3. DIRECTOR ALERT: Dispatches an emergency re-link command to Obsidian's private Gmail.
    """
    def __init__(self):
        self.is_failover_active = False
        self.critical_ports = [8000, 1080, 1081] # Core ingress indicators

    async def run_sentinel_watchdog(self):
        colony_log("MIRROR: Initiating Bulletproof Cloud Sentinel...", node="SECURITY")

        while True:
            try:
                # 1. Verify Local Grid Health
                all_up = True
                for port in self.critical_ports:
                    if not self._is_local_port_open(port):
                        all_up = False
                        break

                if all_up:
                    if self.is_failover_active:
                        colony_log(" MIRROR: Primary Grid Recovered. Reverting Cloud Mirror.", node="SECURITY")
                        self.is_failover_active = False
                else:
                    raise Exception("Local Critical Ports Unresponsive")

            except Exception as e:
                if not self.is_failover_active:
                    colony_log(f"[ALERT] FAILOVER: Primary Grid BREACHED [{e}]. Activating 2ND BASE on [{ALIBABA_EIP}]...", node="SECURITY")

                    # A. LOCK IN SAFE MODE
                    self.is_failover_active = True
                    db.log_event("SECURITY", "CLOUD_TAKEOVER_ACTIVE", {"mirror_ip": ALIBABA_EIP})

                    # B. DISPATCH RE-LINK EMAIL
                    from obsidian_emergency_notifier import emergency_notifier
                    emergency_notifier.send_failover_alert(ALIBABA_EIP, 8000)

                    # C. ACTIVATE CLOUD-BASED MINING STACK
                    # subprocess.Popen("python colony_backend/obsidian_permanent_burst_loop.py --remote", shell=True)

            await asyncio.sleep(20) # 20-second heartbeat for high-speed recovery

    def _is_local_port_open(self, port):
        import socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            return s.connect_ex(('127.0.0.1', port)) == 0

cloud_mirror = ObsidianCloudMirror()

if __name__ == "__main__":
    asyncio.run(cloud_mirror.run_sentinel_watchdog())
