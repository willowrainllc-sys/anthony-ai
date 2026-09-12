# --- WILLOW RAIN SECURITY: CASH APP GHOST EXECUTOR v1.0 ---
import os
import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright
from swarm_logger import swarm_log
from swarm_persistence import db
from human_stealth_helper import human_stealth
from cookie_monster_vault import cookie_monster

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
SESSION_FILE = PERSONA_VAULT / "cashapp_auth.json"

class CashAppBrowserBot:
    """
    CASH APP GHOST EXECUTOR v1.0:
    Connects directly to Obsidian's Cash App ($obsidianco) via headless web to manage Bitcoin.
    1. ZERO-API VAULTING: Bypasses API restrictions by using vaulted session cookies.
    2. BTC BALANCE SCRAPING: Reads the real-time Bitcoin balance from the Cash App dashboard.
    3. AUTO-SWEEP PREP: Prepares the environment to auto-sell or transfer BTC.
    """
    def __init__(self):
        self.url = "https://cash.app/login"

    async def open_interactive_login_session(self, headless: bool = False) -> dict:
        swarm_log("CASHAPP_BOT: Launching browser session for Cash App login...", node="FINANCE")

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=headless)
                context = await browser.new_context(
                    user_agent=human_stealth.get_random_user_agent(),
                    viewport={"width": 1280, "height": 800}
                )
                page = await context.new_page()

                # INJECT ANTI-BOT STEALTH SCRIPTS
                await human_stealth.inject_stealth_scripts(page)

                print("\n====================================================")
                print("  CASH APP ($obsidianco) INTERACTIVE LOGIN")
                print("====================================================")
                print("1. Enter your phone number or email linked to Cash App.")
                print("2. Enter the confirmation code sent to you.")
                print("3. Once you see your dashboard, CLOSE the browser window.")
                print("4. Your session will be vaulted for the Obsidian Grid.")
                print("====================================================\n")

                await page.goto(self.url, timeout=45000)

                # Monitor until user closes page or browser
                while True:
                    try:
                        if page.is_closed() or not browser.is_connected():
                            break
                        await asyncio.sleep(1.5)
                    except:
                        break

                # Save vaulted session state
                state_data = await context.storage_state(path=str(SESSION_FILE))
                cookie_monster.eat_and_vault_session("cashapp", state_data)

                swarm_log(f" CASHAPP SESSION VAULTED: Secured cookies for $obsidianco.", node="FINANCE")
                await browser.close()
                return {"status": "SUCCESS", "message": "Cash App session vaulted successfully."}
        except Exception as e:
            swarm_log(f"[-] Cash App Session Note: {e}", node="FINANCE")
            return {"status": "ERROR", "message": str(e)}

    async def run_headless_status_check(self) -> dict:
        """Runs background headless status check on Cash App account."""
        if not SESSION_FILE.exists():
            return {"status": "NEEDS_LOGIN"}

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    storage_state=str(SESSION_FILE),
                    user_agent=human_stealth.get_random_user_agent(),
                    viewport={"width": 1280, "height": 800}
                )
                page = await context.new_page()
                await human_stealth.inject_stealth_scripts(page)

                swarm_log("CASHAPP_BOT: Verifying real-time Bitcoin holdings...", node="FINANCE")
                await page.goto("https://cash.app/account", timeout=30000, wait_until="networkidle")

                # --- AGENTIC DAEMON UPGRADE: Self-Healing & Telemetry ---
                interruption = await human_stealth.handle_interruptions(page)
                if interruption == "NEEDS_2FA":
                    await human_stealth.take_learning_snapshot(page, "cashapp", "failed_2fa_wall")
                    await browser.close()
                    return {"status": "NEEDS_2FA", "message": "Hit 2FA or Security wall."}

                await human_stealth.apply_human_jitter(2.0, 4.0)

                # Wait specifically for the balance elements to render
                try:
                    await page.wait_for_selector('text="$"', timeout=10000)
                except: pass

                # --- AGENTIC DAEMON UPGRADE: Hardcode layout for future learning ---
                await human_stealth.take_learning_snapshot(page, "cashapp", "account_dashboard")

                # Scrape page for balance indicators
                title = await page.title()
                content = await page.evaluate("() => document.body.innerText")

                # Basic extraction of the first dollar amount found (usually the main balance)
                import re
                matches = re.findall(r'\$[0-9,]+\.[0-9]{2}', content)
                btc_balance_usd = matches[0] if matches else "$0.00"

                await browser.close()

                return {
                    "status": "SESSION_ACTIVE",
                    "title": title,
                    "portal": "Cash App ($obsidianco)",
                    "btc_balance_usd_est": btc_balance_usd,
                    "learning_telemetry_saved": True
                }
        except Exception as e:
            # AGENTIC FAILURE SNAPSHOT
            try:
                await human_stealth.take_learning_snapshot(page, "cashapp", "error_state")
            except: pass
            return {"status": "ERROR", "error": str(e)}

cashapp_bot = CashAppBrowserBot()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "interactive"
    if mode == "check":
        res = asyncio.run(cashapp_bot.run_headless_status_check())
    else:
        res = asyncio.run(cashapp_bot.open_interactive_login_session(headless=False))
    print("CASHAPP BOT RESULT:", json.dumps(res, indent=2))
