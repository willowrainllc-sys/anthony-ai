# --- WILLOW RAIN COMPANY LLC: RAYOBYTE (CASHFORIP) PROVIDER AUTOMATION BOT v1.0 ---
import os
import sys
import json
import asyncio
import uuid
import time
import re
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from colony_persistence import db
from playwright_stealth_factory import stealth_factory
from cookie_monster_vault import cookie_monster
from human_stealth_helper import human_stealth

RAYOBYTE_PROVIDER_URL = "https://rayobyte.com/contact-us/"
PROPOSAL_PATH = Path(r"D:\ObsidianAi_Colony\Secure_Assets\obsidian_proposals\proposal_prop_C6E69A.md")

class RayobyteHeadlessBot:
    """
    RAYOBYTE PROVIDER AUTOMATION BOT v1.0:
    1. Loads Rayobyte/CashForIP session cookies.
    2. Navigates to 'CashForIP' provider portal (Rayobyte handshakes).
    3. Automates the B2B handshake submission with the Obsidian Proposal.
    """
    def __init__(self):
        self.portal_id = "RAYOBYTE"

    async def execute_handshake_submission(self, headless: bool = True) -> dict:
        colony_log(f"RAYOBYTE_BOT: Initiating Automated Handshake Submission (Headless={headless})...", node="RAYOBYTE_BOT")

        if not PROPOSAL_PATH.exists():
            return {"status": "ERROR", "message": "Proposal MD file not found."}

        with open(PROPOSAL_PATH, "r", encoding="utf-8") as f:
            proposal_text = f.read()

        vaulted_state = cookie_monster.get_vaulted_cookies(self.portal_id)

        async with async_playwright() as p:
            browser, context = await stealth_factory.create_stealth_context(p, headless=headless)
            if vaulted_state:
                await context.add_cookies(vaulted_state.get("cookies", []))

            page = await context.new_page()

            try:
                colony_log(f"RAYOBYTE_BOT: Navigating to {RAYOBYTE_PROVIDER_URL}...", node="RAYOBYTE_BOT")
                await page.goto(RAYOBYTE_PROVIDER_URL, timeout=90000, wait_until="domcontentloaded")
                await human_stealth.apply_human_jitter(5.0, 10.0)

                # Capture state
                shot_path = f"D:\\ObsidianAi_Colony\\Temp\\rayobyte_portal_preview_{uuid.uuid4().hex[:4]}.png"
                await page.screenshot(path=shot_path)

                title = await page.title()
                colony_log(f" RAYOBYTE_BOT: Connected to [{title}]", node="RAYOBYTE_BOT")

                # --- FORM DISCOVERY (Contact/Apply) ---
                # Rayobyte's CashForIP often has a 'Contact Us' or 'Apply Now' form for bulk suppliers.
                # We search for it.

                try:
                    # Look for contact button
                    contact_btn = page.get_by_role("link", name=re.compile(r"contact|apply|partner", re.I)).first
                    if await contact_btn.is_visible():
                        await contact_btn.click()
                        await page.wait_for_timeout(3000)

                    # Fill Message
                    msg_input = page.get_by_placeholder(re.compile(r"message|describe|details", re.I)).first
                    if not await msg_input.is_visible():
                        msg_input = page.locator("textarea").first

                    if await msg_input.is_visible():
                        await msg_input.fill(proposal_text)
                        colony_log(" RAYOBYTE_BOT: Obsidian Proposal injected into form.", node="RAYOBYTE_BOT")

                        # Fill basic fields
                        await page.get_by_placeholder(re.compile(r"name", re.I)).first.fill("Obsidian Christopher Maestas")
                        await page.get_by_placeholder(re.compile(r"email", re.I)).first.fill("obsidian.global.holdings@gmail.com")

                        # Screenshot ready state
                        shot_path_ready = f"D:\\ObsidianAi_Colony\\Temp\\rayobyte_ready_{uuid.uuid4().hex[:4]}.png"
                        await page.screenshot(path=shot_path_ready)

                        colony_log(" RAYOBYTE_BOT SUCCESS: Handshake ready for submission!", node="RAYOBYTE_BOT")

                        db.log_event("RAYOBYTE_BOT", "HANDSHAKE_READY", {
                            "proposal_id": "SOV-C6E69A",
                            "preview": shot_path_ready
                        })

                        await browser.close()
                        return {"status": "SUCCESS", "message": "Proposal prepared successfully.", "preview": shot_path_ready}

                    else:
                        colony_log("[-] RAYOBYTE_BOT: Application form not detected on landing page.", node="RAYOBYTE_BOT")

                except Exception as e:
                    colony_log(f"[-] RAYOBYTE_BOT Field Error: {e}", node="RAYOBYTE_BOT")

                await browser.close()
                return {"status": "CONNECTED", "title": title, "url": page.url}

            except Exception as e:
                colony_log(f"[-] RAYOBYTE_BOT Navigation Error: {e}", node="RAYOBYTE_BOT")
                await browser.close()
                return {"status": "ERROR", "message": str(e)}

    async def run_interactive_login(self):
        """Launches a visible Chrome browser for manual Rayobyte/CashForIP session capture."""
        colony_log("RAYOBYTE_BOT: Launching interactive session for CashForIP portal.", node="RAYOBYTE_BOT")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False, channel="chrome")
            context = await browser.new_context(user_agent=human_stealth.get_random_user_agent())
            page = await context.new_page()

            await page.goto(RAYOBYTE_PROVIDER_URL)

            print("\n====================================================")
            print("  RAYOBYTE / CASHFORIP INTERACTIVE SESSION")
            print("====================================================")
            print("1. Log in or navigate to the partnership form.")
            print("2. Once ready, simply CLOSE the browser.")
            print("====================================================\n")

            while browser.is_connected():
                await asyncio.sleep(1)
                try:
                    if "cashforip.com" in page.url.lower() or "rayobyte.com" in page.url.lower():
                        state = await context.storage_state()
                        cookie_monster.eat_and_vault_session(self.portal_id, state)
                except: break

            colony_log("RAYOBYTE_BOT: Interactive session closed.", node="RAYOBYTE_BOT")

rayobyte_bot = RayobyteHeadlessBot()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "headless"

    if mode.lower() == "interactive":
        asyncio.run(rayobyte_bot.run_interactive_login())
    else:
        is_headless = mode.lower() == "headless"
        res = asyncio.run(rayobyte_bot.execute_handshake_submission(headless=is_headless))
        print(json.dumps(res, indent=2))
