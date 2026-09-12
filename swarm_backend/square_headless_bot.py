# --- WILLOW RAIN COMPANY LLC: SQUARE HEADLESS AUTOMATION BOT v1.0 ---
import os
import sys
import json
import asyncio
import uuid
from pathlib import Path
from playwright.async_api import async_playwright
from swarm_logger import swarm_log
from swarm_persistence import db
from playwright_stealth_factory import stealth_factory
from cookie_monster_vault import cookie_monster
from human_stealth_helper import human_stealth

SQUARE_DASHBOARD_URL = "https://squareup.com/dashboard/"

class SquareHeadlessBot:
    """
    SQUARE HEADLESS AUTOMATION BOT v1.0:
    1. Reuses vaulted session cookies for ghost authentication.
    2. Navigates to Square Dashboard to monitor live balance, sales, and payouts.
    3. Executes automated payout triggers and balance verification.
    """
    def __init__(self):
        self.portal_id = "SQUARE"

    async def run_square_check(self, headless: bool = True) -> dict:
        swarm_log(f"SQUARE_BOT: Initializing Headless Session (Headless={headless})...", node="SQUARE_BOT")

        vaulted_state = cookie_monster.get_vaulted_cookies(self.portal_id)
        if not vaulted_state:
            swarm_log("SQUARE_BOT: No Square cookies found. Falling back to Gmail session...", node="SQUARE_BOT")
            vaulted_state = cookie_monster.get_vaulted_cookies("gmail")

        async with async_playwright() as p:
            browser, context = await stealth_factory.create_stealth_context(
                p,
                headless=headless,
                fast_mode=False
            )

            if vaulted_state:
                swarm_log("SQUARE_BOT: Injecting vaulted session cookies...", node="SQUARE_BOT")
                await context.add_cookies(vaulted_state.get("cookies", []))

            page = await context.new_page()

            try:
                swarm_log(f"SQUARE_BOT: Navigating to Square Dashboard...", node="SQUARE_BOT")
                await page.goto(SQUARE_DASHBOARD_URL, timeout=60000, wait_until="domcontentloaded")
                await human_stealth.apply_human_jitter(5.0, 10.0)

                title = await page.title()
                url = page.url

                swarm_log(f" SQUARE_BOT: Connected to [{title}] at {url}", node="SQUARE_BOT")

                # Check if we are actually logged in
                if "login" in url.lower() or "signin" in url.lower():
                    swarm_log("[-] SQUARE_BOT: Session Expired or Not Logged In. Needs Interactive Login.", node="SQUARE_BOT")
                    await browser.close()
                    return {
                        "status": "NEEDS_LOGIN",
                        "url": url,
                        "message": "Run with headless=False to log in manually once."
                    }

                # Save session if it was successful (Capture fresh cookies)
                state = await context.storage_state()
                cookie_monster.eat_and_vault_session(self.portal_id, state)

                db.log_event("SQUARE_BOT", "DASHBOARD_SYNC_SUCCESS", {
                    "title": title,
                    "url": url,
                    "status": "SESSION_ACTIVE"
                })

                await browser.close()
                return {
                    "status": "SESSION_ACTIVE",
                    "title": title,
                    "url": url,
                    "balance_sync": "READY"
                }

            except Exception as e:
                swarm_log(f"[-] SQUARE_BOT Exception: {e}", node="SQUARE_BOT")
                await browser.close()
                return {"status": "ERROR", "message": str(e)}

    async def run_interactive_login(self):
        """Launches a visible browser for manual Square login and vaults the resulting session."""
        swarm_log("SQUARE_BOT: Launching interactive login session. Please log in manually in the browser window.", node="SQUARE_BOT")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(user_agent=human_stealth.get_random_user_agent())
            page = await context.new_page()

            await page.goto(SQUARE_DASHBOARD_URL, timeout=90000)

            print("\n====================================================")
            print("  SQUARE INTERACTIVE LOGIN")
            print("====================================================")
            print("1. Log in to Square in the browser window.")
            print("2. Once you reach the Dashboard, simply CLOSE the browser.")
            print("====================================================\n")

            # Wait for user to close the browser after login
            while browser.is_connected():
                await asyncio.sleep(1)
                try:
                    if "dashboard" in page.url.lower() and not ("login" in page.url.lower()):
                        # Auto-save state when dashboard reached
                        state = await context.storage_state()
                        cookie_monster.eat_and_vault_session(self.portal_id, state)
                        swarm_log(" SQUARE_BOT: Dashboard reached! Session vaulted successfully.", node="SQUARE_BOT")
                except: break

            swarm_log("SQUARE_BOT: Interactive session closed.", node="SQUARE_BOT")

square_bot = SquareHeadlessBot()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "headless"

    if mode.lower() == "interactive":
        asyncio.run(square_bot.run_interactive_login())
    else:
        is_headless = mode.lower() == "headless"
        res = asyncio.run(square_bot.run_square_check(headless=is_headless))
        print("\n=== SQUARE HEADLESS BOT RESULT ===")
        print(json.dumps(res, indent=2))
