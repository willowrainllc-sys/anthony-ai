# --- WILLOW RAIN COMPANY LLC: GMAIL B2B HANDSHAKE MONITOR v1.0 ---
import os
import sys
import json
import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright
from swarm_logger import swarm_log
from swarm_persistence import db
from playwright_stealth_factory import stealth_factory
from cookie_monster_vault import cookie_monster
from human_stealth_helper import human_stealth

GMAIL_URL = "https://mail.google.com/mail/u/0/#search/Geonode+OR+Rayobyte+OR+Obsidian Grid"

class GmailHandshakeMonitor:
    """
    GMAIL B2B HANDSHAKE MONITOR v1.0:
    1. Reuses vaulted Gmail session cookies.
    2. Scans for approval/onboarding emails from Geonode, Rayobyte, and Obsidian Grid.
    3. Auto-logs the approval status to unblock real-world traffic routing.
    """
    async def scan_for_b2b_approvals(self, headless: bool = True) -> dict:
        swarm_log(f"GMAIL_MONITOR: Scanning inbox for B2B approval signals (Headless={headless})...", node="GMAIL_MONITOR")

        vaulted_state = cookie_monster.get_vaulted_cookies("gmail")
        if not vaulted_state:
            return {"status": "ERROR", "message": "Gmail session cookies not found."}

        async with async_playwright() as p:
            browser, context = await stealth_factory.create_stealth_context(p, headless=headless)
            await context.add_cookies(vaulted_state.get("cookies", []))

            page = await context.new_page()

            try:
                swarm_log("GMAIL_MONITOR: Navigating to search results...", node="GMAIL_MONITOR")
                await page.goto(GMAIL_URL, timeout=90000, wait_until="domcontentloaded")
                await asyncio.sleep(10) # Wait for results to populate

                # Capture search result state
                await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\gmail_b2b_search.png")

                content = await page.content()

                # Check for approval indicators
                found_approval = False
                found_partner = None

                for partner in ["Geonode", "Rayobyte", "Obsidian Grid"]:
                    if partner.lower() in content.lower():
                        if "approved" in content.lower() or "welcome" in content.lower() or "onboarding" in content.lower():
                            found_approval = True
                            found_partner = partner
                            break

                if found_approval:
                    swarm_log(f" GMAIL_MONITOR SUCCESS: Found B2B approval signal from [{found_partner}]!", node="GMAIL_MONITOR")
                    db.log_event("GMAIL_MONITOR", "B2B_APPROVAL_DETECTED", {"partner": found_partner})
                    return {"status": "APPROVAL_FOUND", "partner": found_partner}
                else:
                    swarm_log("GMAIL_MONITOR: No new approval signals detected yet. Pipeline remains ARMED.", node="GMAIL_MONITOR")
                    return {"status": "NEGOTIATING", "message": "Awaiting Handshake partner handshake."}

            except Exception as e:
                swarm_log(f"[-] GMAIL_MONITOR Error: {e}", node="GMAIL_MONITOR")
                return {"status": "ERROR", "message": str(e)}
            finally:
                await browser.close()

monitor = GmailHandshakeMonitor()

if __name__ == "__main__":
    monitor = GmailHandshakeMonitor()
    asyncio.run(monitor.scan_for_b2b_approvals(headless=True))
