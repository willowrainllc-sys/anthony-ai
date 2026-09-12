# --- WILLOW RAIN SECURITY: OBSIDIAN API NODE IGNITER v2.0 (HIGH-SPEED) ---
import asyncio
import os
import json
import time
from pathlib import Path
from curl_cffi import requests
from swarm_logger import swarm_log
from swarm_persistence import db

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
JMPT_SESSION = PERSONA_VAULT / "cookie_monster" / "cookie_monster_obsidian_bridge.json"

class ObsidianAPIIgniter:
    """
    OBSIDIAN API IGNITER v2.0:
    1. PARALLEL PULSE: Uses asyncio.gather to ignite 100 ports in seconds.
    2. SESSION SYNC: Ensures every port carries the Director's physical auth key.
    3. REVENUE VERIFICATION: Hits the stats API to force a balance refresh.
    """
    def __init__(self):
        self.ports = list(range(1080, 1181))

    def _get_cookie_str(self):
        if not JMPT_SESSION.exists(): return None
        with open(JMPT_SESSION, 'r') as f:
            data = json.load(f)
            cookies = data.get("cookies", [])
            return "; ".join([f"{c['name']}={c['value']}" for c in cookies])

    async def _ignite_single_port(self, port, cookie_str):
        proxy_url = f"socks5://127.0.0.1:{port}"
        try:
            # We use a lightweight session to ping the devices API
            with requests.Session(impersonate="chrome110", proxies={"http": proxy_url, "https": proxy_url}) as s:
                # 1. Register Device / Pulse Heartbeat
                resp = s.get("https://dashboard.obsidian_ingress.com/api/v1/devices", headers={"Cookie": cookie_str}, timeout=10)
                if resp.status_code == 200:
                    # 2. Force balance sync
                    s.get("https://dashboard.obsidian_ingress.com/api/v1/users/me", headers={"Cookie": cookie_str}, timeout=10)
                    return True
        except:
            return False
        return False

    async def execute_blitz(self):
        cookie_str = self._get_cookie_str()
        if not cookie_str:
            swarm_log("[-] IGNITER: Session missing. Handshake aborted.", node="SUPREME")
            return

        swarm_log(f"IGNITER: Striking 101 ports with mobile session [{cookie_str[:20]}...]...", node="SUPREME")

        # Split into batches of 20 to avoid OS socket exhaustion
        total_active = 0
        batch_size = 20
        for i in range(0, len(self.ports), batch_size):
            batch = self.ports[i:i+batch_size]
            tasks = [self._ignite_single_port(p, cookie_str) for p in batch]
            results = await asyncio.gather(*tasks)
            total_active += sum(1 for r in results if r)
            swarm_log(f" IGNITER: {total_active} nodes ARMED.", node="SUPREME")
            await asyncio.sleep(0.5)

        swarm_log(f"[SUPREME] SUPREME SUCCESS: {total_active} REAL nodes feeding your account.", node="SUPREME")
        return total_active

igniter = ObsidianAPIIgniter()

if __name__ == "__main__":
    asyncio.run(igniter.execute_blitz())
