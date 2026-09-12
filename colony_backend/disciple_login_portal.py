# --- WILLOW RAIN SECURITY: DISCIPLE LOGIN PORTAL v1.0 ---
import asyncio
import os
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from human_stealth_helper import human_stealth
from cookie_monster_vault import cookie_monster

class DiscipleLoginPortal:
    """
    DISCIPLE LOGIN PORTAL v1.0:
    Allows Obsidian to manually log in to the "Honey Comb" portals.
    This captures real session cookies so the bots can actually PLAY and EARN.
    """
    def __init__(self):
        self.portals = {
            "FREECASH": "https://obsidian_rewards.com/login",
            "INBOXDOLLARS": "https://www.obsidian_rewards.com/login",
            "SWAGBUCKS": "https://www.obsidian_rewards.com/login",
            "IPSOS": "https://www.ipsosisay.com/en-us/user/login",
            "OBSIDIAN_BRIDGE": "https://obsidian_bridge.io/"
        }

    async def open_interactive_login(self, portal_id: str):
        url = self.portals.get(portal_id.upper())
        if not url:
            print(f"Error: Portal {portal_id} not found.")
            return

        colony_log(f"LOGIN_PORTAL: Opening interactive session for [{portal_id}]...", node="SECURITY")

        async with async_playwright() as p:
            # EMULATE MOBILE PHONE (Pixel 7)
            device = p.devices['Pixel 7']
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(**device)
            page = await context.new_page()

            print(f"\n[!] ACTION REQUIRED: Log in to {portal_id} in the browser window.")
            print("[!] Once logged in and the dashboard is visible, CLOSE the browser window.\n")

            await page.goto(url)

            # Wait for window to close
            while True:
                try:
                    if page.is_closed() or not browser.is_connected():
                        break
                    await asyncio.sleep(1)
                except: break

            # Capture and Vault Cookies
            state = await context.storage_state()
            cookie_monster.eat_and_vault_session(portal_id.lower(), state)

            colony_log(f" LOGIN_PORTAL: Session for [{portal_id}] successfully vaulted.", node="SECURITY")
            await browser.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        portal = sys.argv[1]
        portal_mgr = DiscipleLoginPortal()
        asyncio.run(portal_mgr.open_interactive_login(portal))
    else:
        print("Usage: python disciple_login_portal.py <PORTAL_ID>")
        print("IDs: FREECASH, INBOXDOLLARS, SWAGBUCKS, IPSOS")
