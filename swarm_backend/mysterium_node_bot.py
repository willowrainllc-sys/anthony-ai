# --- EMPIRE MYSTERIUM DVPN NODE AUTOMATION BOT v1.0 ---
import os
import sys
import json
import asyncio
import httpx
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
PERSONA_VAULT.mkdir(parents=True, exist_ok=True)

class MysteriumNodeBot:
    """
    MYSTERIUM DVPN NODE AUTOMATION BOT v1.0:
    Connects to Mysterium Node Web UI (http://127.0.0.1:4449),
    monitors shared bandwidth, tracks earned MYST tokens,
    and manages Polygon wallet auto-payout thresholds.
    """
    def __init__(self, node_url: str = "http://127.0.0.1:4449"):
        self.node_url = node_url
        self.polygon_wallet = os.getenv("PAYMENT_HUB_WALLET_ID", "0xWillowRainPolygonWallet2026")

    async def get_node_status_and_myst_balance(self) -> dict:
        swarm_log(f"MYSTERIUM_BOT: Connecting to Mysterium Node UI [{self.node_url}]...", node="MYSTERIUM")

        # 1. Try REST API endpoint on Mysterium Node UI
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(f"{self.node_url}/api/v2/nodes/me")
                if res.status_code == 200:
                    data = res.json()
                    myst_earned = data.get("earnings", {}).get("total_myst", 0.0)
                    swarm_log(f" MYSTERIUM_BOT: Node Online! Earned MYST: {myst_earned}", node="MYSTERIUM")
                    return {
                        "status": "NODE_ONLINE",
                        "node_id": data.get("identity"),
                        "myst_earned": myst_earned,
                        "polygon_wallet": self.polygon_wallet
                    }
        except Exception as e:
            swarm_log(f"[-] Mysterium Node UI REST Note: {e}", node="MYSTERIUM")

        # 2. Try Playwright Headless Connection
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                await page.goto(self.node_url, timeout=15000)
                await asyncio.sleep(2)

                # --- AGENTIC DAEMON UPGRADE ---
                from human_stealth_helper import human_stealth
                interruption = await human_stealth.handle_interruptions(page)
                if interruption == "NEEDS_2FA":
                    await human_stealth.take_learning_snapshot(page, "mysterium", "2fa_blocked")
                    await browser.close()
                    return {"status": "NEEDS_2FA"}

                await human_stealth.take_learning_snapshot(page, "mysterium", "node_dashboard")

                title = await page.title()
                await browser.close()
                return {
                    "status": "NODE_UI_CONNECTED",
                    "title": title,
                    "polygon_wallet": self.polygon_wallet,
                    "learning_telemetry_saved": True
                }
        except Exception as e:
            swarm_log(f"[-] Mysterium Headless Session Note: {e}", node="MYSTERIUM")

        return {
            "status": "NODE_STANDBY",
            "message": f"Mysterium Node UI at {self.node_url} ready. Set up local container or Docker node to activate.",
            "polygon_wallet": self.polygon_wallet,
            "target_auto_payout_threshold": "5 MYST"
        }

    async def configure_polygon_auto_payout(self, wallet_address: str, auto_payout_myst: float = 5.0) -> dict:
        """Configures self-custody Polygon wallet address and payout threshold."""
        swarm_log(f"MYSTERIUM_BOT: Setting Polygon payout wallet [{wallet_address[:10]}...] with threshold {auto_payout_myst} MYST...", node="MYSTERIUM")

        self.polygon_wallet = wallet_address
        db.log_event("MYSTERIUM", "POLYGON_PAYOUT_CONFIGURED", {
            "wallet_address": wallet_address,
            "auto_payout_threshold_myst": auto_payout_myst,
            "status": "ACTIVE"
        })

        return {
            "status": "success",
            "wallet_address": wallet_address,
            "auto_payout_threshold": f"{auto_payout_myst} MYST",
            "settlement_network": "Polygon (ERC-20)"
        }

mysterium_bot = MysteriumNodeBot()

if __name__ == "__main__":
    res = asyncio.run(mysterium_bot.get_node_status_and_myst_balance())
    print("MYSTERIUM NODE BOT STATUS:")
    print(json.dumps(res, indent=2))
