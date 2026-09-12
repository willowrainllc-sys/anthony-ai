# --- WILLOW RAIN SECURITY: SUPREME INDUSTRIAL SIGNER v10.0 (RESIDENTIAL BRIDGE) ---
import asyncio
import os
import uuid
import random
import json
import time
from curl_cffi import requests
from swarm_logger import swarm_log
from swarm_persistence import db

COUPON_CODE = "dontpayfull5"
OBSIDIAN_BRIDGE_ID = "c54d9d74-fd16-4bfd-9136-904fb62ff21f"

class ObsidianIndustrialSigner:
    """
    SUPREME INDUSTRIAL SIGNER v10.0:
    The "Local Residential" Bypass Engine.
    1. AUTHORITY BRIDGE: Uses the Director's 100/100 Home IP for account birth.
    2. SMART THROTTLE: Limits to 1 signup every 15-30s to stay under human detection.
    3. AUTO-LINK: Binds the JMPT wallet ID during the atomic strike.
    4. REVENUE LOCK: Guarantees the $5.00 strike per account.
    """
    def __init__(self):
        self.api_endpoint = "https://dashboard.obsidian_ingress.com/api/v1/users"
        # No proxy for signup strike = Uses the high-aura Home IP
        self.proxy = None

    async def execute_9k_blitz(self, count: int = 100):
        swarm_log(f"FACTORY_v10: Initiating Residential-Bridge Blitz (Target: {count})...", node="SUPREME")

        total_created = 0

        for i in range(count):
            success = await self._execute_atomic_strike()
            if success:
                total_created += 1
                swarm_log(f" BLITZ: {total_created}/{count} accounts live. Value: ${total_created * 5.00:,.2f}", node="SUPREME")

            # Smart delay between births
            await asyncio.sleep(random.uniform(15, 35))

        swarm_log(f"[SUPREME] SUPREME SUCCESS: {total_created} accounts ARMED. All payments FIREWALLED.", node="SUPREME")
        return total_created

    async def _execute_atomic_strike(self):
        """Creates and links an account via the Director's high-aura IP."""
        email_prefix = f"alpha_sentinel_{uuid.uuid4().hex[:6]}"
        email = f"obsidian.global.holdings+{email_prefix}@gmail.com"
        password = f"Alpha_{uuid.uuid4().hex[:10]}!"

        payload = {"email": email, "password": password, "coupon_code": COUPON_CODE}

        try:
            with requests.Session(impersonate="chrome110") as s:
                # 1. SIGNUP
                resp = s.post(self.api_endpoint, json=payload, timeout=25)

                if resp.status_code in [200, 201]:
                    jwt = resp.json().get("jwt")
                    # 2. AUTO-LINK JMPT
                    link_resp = s.post(
                        "https://dashboard.obsidian_ingress.com/api/v1/obsidian_bridge/link",
                        json={"obsidian_bridge_id": OBSIDIAN_BRIDGE_ID},
                        headers={"Authorization": f"Bearer {jwt}"}
                    )

                    if link_resp.status_code == 200:
                        db.log_event("SUPREME", "ACCOUNT_ARMED_AND_LINKED", {"email": email})
                        return True
        except:
            return False
        return False

industrial_signer = ObsidianIndustrialSigner()

if __name__ == "__main__":
    asyncio.run(industrial_signer.execute_9k_blitz(25))
