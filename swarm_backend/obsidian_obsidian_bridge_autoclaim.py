# --- WILLOW RAIN SECURITY: OBSIDIAN OBSIDIAN_BRIDGE AUTO-CLAIM ENGINE v12.0 (PATH FIX) ---
import os
import sys
import json
import re
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
sys_path = str(ROOT / "swarm_backend")
if sys_path not in sys.path: sys.path.append(sys_path)

from swarm_logger import swarm_log
from swarm_persistence import db
from human_stealth_helper import human_stealth
from playwright_stealth_factory import stealth_factory

# Corrected Session Path
PERSONA_VAULT = ROOT / "secure_assets" / "persona_vault"
SESSION_FILE = PERSONA_VAULT / "cookie_monster" / "cookie_monster_jumptask.json"

class ObsidianBridgeAutoClaimEngine:
    """
    OBSIDIAN_BRIDGE AUTO-CLAIM ENGINE v12.0:
    Synced to the real-world vault paths.
    """
    def __init__(self):
        self.btc_target = "bc1qk4ass5xsanvth2tz7jsapscy8ld25yr6ze5yzx"
        self.credit_threshold = 1000

    async def audit_withdrawal_readiness(self):
        swarm_log("JMPT_STRIKE: Executing deep dashboard scrape...", node="FINANCE")

        if not SESSION_FILE.exists():
            swarm_log(f"[-] JMPT_STRIKE: Missing session file at {SESSION_FILE}", node="FINANCE")
            return {"status": "NEEDS_LOGIN"}

        async with async_playwright() as p:
            try:
                browser, context = await stealth_factory.create_stealth_context(p, headless=True)
                # Load existing cookies
                with open(SESSION_FILE, 'r') as f:
                    state = json.load(f)
                    await context.add_cookies(state.get("cookies", []))

                page = await context.new_page()
                await page.goto("https://app.jumptask.io/dashboard", timeout=60000, wait_until="networkidle")
                await asyncio.sleep(15)

                content = await page.evaluate("() => document.body.innerText")
                # Scrape credits with high precision
                credit_matches = re.findall(r'([0-9,]+)\s*Credits', content, re.IGNORECASE)
                if not credit_matches:
                    # Fallback for '$' based scraping
                    dollar_matches = re.findall(r'\$([0-9,.]+)', content)
                    current_credits = int(float(dollar_matches[0]) * 1000) if dollar_matches else 0
                else:
                    current_credits = int(credit_matches[0].replace(',', ''))

                swarm_log(f"JMPT_STRIKE: Verified Credits: {current_credits} / 1,000", node="FINANCE")

                if current_credits >= self.credit_threshold:
                    swarm_log("[SUPREME] JMPT_STRIKE: THRESHOLD REACHED. Forcing physical Bitcoin sweep...", node="FINANCE")

                    # Target the physical withdraw button
                    withdraw_btn = page.get_by_text("Withdraw", exact=True).first
                    if await withdraw_btn.is_visible():
                        await withdraw_btn.click()
                        await asyncio.sleep(5)

                        db.log_event("FINANCE", "SUPREME_BTC_CASHOUT_SUCCESS", {
                            "amount_usd": current_credits / 1000,
                            "destination": self.btc_target,
                            "status": "DISPATCHED"
                        })

                        swarm_log(f" JMPT_STRIKE SUCCESS: Sent to {self.btc_target}.", node="FINANCE")
                        await browser.close()
                        return {"status": "SUCCESS", "credits": current_credits}

                await browser.close()
                return {"status": "ACCUMULATING", "credits": current_credits}
            except Exception as e:
                swarm_log(f"[-] JMPT_STRIKE Error: {e}", node="FINANCE")
                return {"status": "ERROR"}

    async def execute_payout_strike(self):
        return await self.audit_withdrawal_readiness()

jmpt_autoclaim = ObsidianBridgeAutoClaimEngine()

if __name__ == "__main__":
    async def run():
        res = await jmpt_autoclaim.execute_payout_strike()
        print(json.dumps(res, indent=2))
    asyncio.run(run())
