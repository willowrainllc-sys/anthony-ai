# --- WILLOW RAIN SECURITY: OBSIDIAN GMAIL MONITOR & AUTO-VERIFY v1.0 ---
import asyncio
import os
import sys
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from human_stealth_helper import human_stealth

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
SESSION_FILE = PERSONA_VAULT / "cookie_monster" / "cookie_monster_gmail.json"

class ObsidianGmailMonitor:
    """
    OBSIDIAN GMAIL MONITOR v1.0:
    Automates the verification of 1,800+ Honeycomb accounts.
    1. GHOST ACCESS: Uses vaulted Gmail cookies to enter the inbox.
    2. LINK SNIPING: Identifies 'Confirm your email' messages from Obsidian Ingress.
    3. AUTO-CLICK: Opens the verification link to finalize the $5.00 account.
    """
    async def run_verification_sweep(self):
        colony_log("GMAIL_MONITOR: Initiating account verification sweep...", node="SECURITY")

        if not SESSION_FILE.exists():
            colony_log("[-] GMAIL_MONITOR: No session keys found.", node="SECURITY")
            return False

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(SESSION_FILE), user_agent=human_stealth.get_random_user_agent())
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            try:
                # 1. Access Gmail
                await page.goto("https://mail.google.com/mail/u/0/#inbox", timeout=60000)
                await asyncio.sleep(5)

                # 2. Search for Obsidian Ingress Verification Emails
                colony_log("GMAIL_MONITOR: Searching for 'Confirm your email' signals...", node="SECURITY")

                # Robust Search Bar Discovery
                search_bar = page.get_by_placeholder("Search mail").first
                if await search_bar.is_visible():
                    await search_bar.fill("Obsidian Ingress Confirm your email")
                else:
                    await page.fill('input[aria-label="Search mail"]', "Obsidian Ingress Confirm your email")

                await page.keyboard.press("Enter")
                await asyncio.sleep(8) # Extra time for Gmail's slow search

                # 3. Click the first unread message
                # Note: This is simplified. In production, we'd loop through all matches.
                messages = page.locator("tr.unread")
                count = await messages.count()
                colony_log(f"GMAIL_MONITOR: Found {count} unread verification signals.", node="SECURITY")

                for i in range(count):
                    await messages.nth(i).click()
                    await asyncio.sleep(3)

                    # 4. Find and Click the verification link
                    # Typically a big button or a direct link
                    verify_link = page.locator('a:has-text("Verify email")').first
                    if await verify_link.count() > 0:
                        url = await verify_link.get_attribute("href")
                        colony_log(f" GMAIL_MONITOR: Verification link sniped: {url[:50]}...", node="SECURITY")
                        # We use a separate context for the verification to prevent session leaks
                        await self._click_verification_link(url)

                    # Go back to inbox
                    await page.goto("https://mail.google.com/mail/u/0/#inbox", timeout=30000)
                    await asyncio.sleep(2)

                await browser.close()
                return True
            except Exception as e:
                colony_log(f"[-] GMAIL_MONITOR ERROR: {e}", node="SECURITY")
                await browser.close()
                return False

    async def _click_verification_link(self, url: str):
        """Clicks the verification link using a temporary ghost context."""
        async with async_playwright() as p:
            # We must use a proxy for the verification to match the account's IP
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            await asyncio.sleep(5)
            await browser.close()

gmail_monitor = ObsidianGmailMonitor()

if __name__ == "__main__":
    asyncio.run(gmail_monitor.run_verification_sweep())
