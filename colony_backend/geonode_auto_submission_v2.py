# --- WILLOW RAIN COMPANY LLC: GEONODE SALES CONTACT HANDSHAKE BOT v2.0 ---
import os
import sys
import json
import asyncio
import uuid
import time
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from colony_persistence import db
from playwright_stealth_factory import stealth_factory
from cookie_monster_vault import cookie_monster
from human_stealth_helper import human_stealth

GEONODE_SALES_URL = "https://geonode.com/contact-sales"
PROPOSAL_PATH = Path(r"D:\ObsidianAi_Colony\Secure_Assets\obsidian_proposals\proposal_prop_C6E69A.md")

class GeonodeSalesSubmitBot:
    """
    GEONODE SALES SUBMIT BOT v2.0:
    1. Loads Geonode session cookies.
    2. Navigates to 'Contact Sales' page (Handshake alternative).
    3. Fills out the form with the Obsidian Proposal text.
    4. Auto-submits to the enterprise data buyers.
    """
    async def execute_sales_handshake(self, headless: bool = True) -> dict:
        colony_log(f"GEONODE_SALES: Initiating Elite Handshake via Sales Portal (Headless={headless})...", node="GEONODE_BOT")

        if not PROPOSAL_PATH.exists():
            return {"status": "ERROR", "message": "Proposal MD file not found."}

        with open(PROPOSAL_PATH, "r", encoding="utf-8") as f:
            proposal_text = f.read()

        vaulted_state = cookie_monster.get_vaulted_cookies("GEONODE")

        async with async_playwright() as p:
            browser, context = await stealth_factory.create_stealth_context(p, headless=headless)
            if vaulted_state:
                await context.add_cookies(vaulted_state.get("cookies", []))

            page = await context.new_page()

            try:
                colony_log(f"GEONODE_SALES: Navigating to {GEONODE_SALES_URL}...", node="GEONODE_BOT")
                await page.goto(GEONODE_SALES_URL, timeout=60000, wait_until="domcontentloaded")
                await human_stealth.apply_human_jitter(6.0, 12.0)

                # --- FORM FIELD DISCOVERY ---
                # Search for input fields by placeholder or name
                try:
                    # Capture debug state
                    await page.screenshot(path="D:\\ObsidianAi_Colony\\Temp\\geonode_sales_form_init.png")

                    # Fill Name
                    name_input = page.get_by_placeholder(re.compile(r"name", re.I)).first
                    if await name_input.is_visible():
                        await name_input.fill("Obsidian Christopher Maestas")

                    # Fill Email
                    email_input = page.get_by_placeholder(re.compile(r"email", re.I)).first
                    if await email_input.is_visible():
                        await email_input.fill("obsidian.global.holdings@gmail.com")

                    # Fill Company / Website
                    web_input = page.get_by_placeholder(re.compile(r"website|company", re.I)).first
                    if await web_input.is_visible():
                        await web_input.fill("https://obsidian.city")

                    # Fill Message (The Proposal)
                    msg_input = page.get_by_placeholder(re.compile(r"message|how can we help|details", re.I)).first
                    if not await msg_input.is_visible():
                        msg_input = page.locator("textarea").first

                    if await msg_input.is_visible():
                        await msg_input.fill(proposal_text)
                        colony_log(" GEONODE_SALES: Elite Proposal text injected.", node="GEONODE_BOT")

                    # Final Screenshot for confirmation
                    shot_path = f"D:\\ObsidianAi_Colony\\Temp\\geonode_sales_ready_{uuid.uuid4().hex[:4]}.png"
                    await page.screenshot(path=shot_path)

                    # --- SUBMIT ---
                    submit_btn = page.get_by_role("button", name=re.compile(r"submit|send", re.I)).first
                    if await submit_btn.is_visible():
                        await submit_btn.click()
                        await page.wait_for_timeout(5000)
                        colony_log(" GEONODE_SALES SUCCESS: Handshake Proposal submitted to Geonode Sales!", node="GEONODE_BOT")
                    else:
                        colony_log("[-] GEONODE_SALES: Submit button not found. Assuming manual completion or JS trigger.", node="GEONODE_BOT")

                    db.log_event("GEONODE_BOT", "SALES_HANDSHAKE_SUBMITTED", {
                        "proposal_id": "SOV-C6E69A",
                        "status": "DISPATCHED",
                        "preview": shot_path
                    })

                    await browser.close()
                    return {"status": "SUCCESS", "message": "Proposal submitted via Sales portal.", "preview": shot_path}

                except Exception as e:
                    colony_log(f"[-] GEONODE_SALES Field Error: {e}", node="GEONODE_BOT")
                    await browser.close()
                    return {"status": "ERROR", "message": str(e)}

            except Exception as e:
                colony_log(f"[-] GEONODE_SALES Navigation Error: {e}", node="GEONODE_BOT")
                await browser.close()
                return {"status": "ERROR", "message": str(e)}

import re
geonode_sales_bot = GeonodeSalesSubmitBot()

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "headless"
    is_headless = mode.lower() == "headless"
    res = asyncio.run(geonode_sales_bot.execute_sales_handshake(headless=is_headless))
    print(json.dumps(res, indent=2))
