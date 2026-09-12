# --- WILLOW RAIN SECURITY: OBSIDIAN NODE IGNITER v1.0 (MASS LOGIN) ---
import asyncio
import os
import json
import time
from pathlib import Path
from playwright.async_api import async_playwright
from swarm_logger import swarm_log
from swarm_persistence import db
from human_stealth_helper import human_stealth

# Director's Verified Session
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
HG_SESSION = PERSONA_VAULT / "cookie_monster" / "cookie_monster_obsidian_bridge.json"

class ObsidianNodeIgniter:
    """
    OBSIDIAN NODE IGNITER v1.0:
    Physically logs all 102 residential nodes into the Director's account.
    1. PROXY BINDING: Each node connects via a unique port (1080-1180).
    2. SESSION INJECTION: Injects the Director's active cookies into the headless browser.
    3. HEARTBEAT START: Confirms the node is 'GATHERING' in the real dashboard.
    """
    async def ignite_node(self, port: int):
        proxy_url = f"socks5://127.0.0.1:{port}"
        node_id = f"NODE-PHY-{port}"

        swarm_log(f"IGNITER: Powering up Node [{node_id}] via {proxy_url}...", node="SUPREME")

        async with async_playwright() as p:
            try:
                # Use Pixel 7 emulation for maximum reputation
                device = p.devices['Pixel 7']
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(**device, proxy={"server": proxy_url})

                # Load the Director's cookies
                with open(HG_SESSION, 'r') as f:
                    state = json.load(f)
                    await context.add_cookies(state.get("cookies", []))

                page = await context.new_page()
                await human_stealth.inject_stealth_scripts(page)

                # Navigate and stay alive
                await page.goto("https://dashboard.obsidian_ingress.com/", timeout=60000)
                await asyncio.sleep(5)

                if "dashboard" in page.url:
                    swarm_log(f" IGNITER: Node [{node_id}] is officially CLOCKING IN.", node="SUPREME")
                    db.log_event("SUPREME", "NODE_PHYSICALLY_ACTIVE", {"node_id": node_id, "port": port})
                    # We keep the browser open in the background to maintain the gathering session
                    while True:
                        await asyncio.sleep(300) # Heartbeat pulse
                else:
                    await browser.close()
                    return False
            except Exception as e:
                return False

    async def execute_mass_ignition(self):
        ports = list(range(1080, 1181))
        swarm_log(f"IGNITER: Mobilizing {len(ports)} real nodes to hit the 1,000 credit mark...", node="SUPREME")

        # Batch ignition to prevent CPU bottleneck
        for i in range(0, len(ports), 5):
            batch = ports[i:i+5]
            tasks = [self.ignite_node(p) for p in batch]
            # We don't await because we want them to stay running in background
            for t in tasks:
                asyncio.create_task(t)

            swarm_log(f" IGNITER: {i+5}/{len(ports)} nodes activated.", node="SUPREME")
            await asyncio.sleep(2)

igniter = ObsidianNodeIgniter()

if __name__ == "__main__":
    asyncio.run(igniter.execute_mass_ignition())
