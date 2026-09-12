# --- WILLOW RAIN COMPANY LLC: GMAIL GIFT CARD CODE HARVESTER v1.0 ---
import os
import sys
import json
import asyncio
import re
import time
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from colony_persistence import db
from playwright_stealth_factory import stealth_factory
from cookie_monster_vault import cookie_monster
from human_stealth_helper import human_stealth

GMAIL_SEARCH_URL = "https://mail.google.com/mail/u/0/#search/label%3Aunread+(%22gift+card%22+OR+%22reward+code%22+OR+%22redeem%22+OR+%22voucher%22+OR+%22claim%22)"

class GmailCodeHarvester:
    """
    GMAIL GIFT CARD CODE HARVESTER v1.0:
    1. USES VAULTED GMAIL COOKIES to access obsidian.global.holdings@gmail.com.
    2. SCANS UNREAD EMAILS for gift card keywords.
    3. EXTRACTS REAL CODES using regex patterns (16-digit alphanumeric).
    4. VAULTS THE CODES in the local database for Obsidian Christopher Maestas to redeem.
    """
    async def harvest_codes_from_inbox(self, headless: bool = True) -> int:
        colony_log(f"HARVESTER: Initiating real-world code extraction from Gmail (Headless={headless})...", node="HARVESTER")

        vaulted_state = cookie_monster.get_vaulted_cookies("gmail")
        if not vaulted_state:
            colony_log("[-] HARVESTER: Gmail session cookies not found.", node="HARVESTER")
            return 0

        async with async_playwright() as p:
            browser, context = await stealth_factory.create_stealth_context(p, headless=headless)
            await context.add_cookies(vaulted_state.get("cookies", []))

            page = await context.new_page()

            try:
                colony_log("HARVESTER: Navigating to filtered inbox...", node="HARVESTER")
                await page.goto(GMAIL_SEARCH_URL, timeout=90000, wait_until="networkidle")
                await asyncio.sleep(8)

                # Capture search results for audit
                await page.screenshot(path="D:\\ObsidianAi_Colony\\Temp\\gmail_harvest_scan.png")

                # 1. Get all unread email rows
                email_rows = page.locator('tr.zA').all()
                count = await email_rows
                colony_log(f"HARVESTER: Found {len(count)} potential reward emails.", node="HARVESTER")

                codes_found = 0

                # 2. Iterate through emails and extract content
                for i in range(min(len(count), 5)): # Process top 5 unread
                    try:
                        await count[i].click()
                        await asyncio.sleep(5)

                        email_body = await page.inner_text("div.a3s")

                        # 3. Regex Extraction Logic (Common Gift Card Formats)
                        # Pattern: 16-char alphanumeric, e.g., ABCD-1234-EFGH-5678
                        patterns = [
                            r'[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}',
                            r'[A-Z0-9]{16}',
                            r'[A-Z0-9]{12}'
                        ]

                        for p_regex in patterns:
                            matches = re.findall(p_regex, email_body)
                            for code in matches:
                                if self._vault_code(code, email_body):
                                    codes_found += 1

                        # Go back to search
                        await page.keyboard.press("u") # Shortcut for back to thread list
                        await asyncio.sleep(3)
                    except: continue

                colony_log(f" HARVESTER SUCCESS: Locked {codes_found} new codes into the Obsidian Vault.", node="HARVESTER")
                return codes_found

            except Exception as e:
                colony_log(f"[-] HARVESTER ERROR: {e}", node="HARVESTER")
                return 0
            finally:
                await browser.close()

    def _vault_code(self, code: str, context_text: str) -> bool:
        """Saves the extracted code to the local database."""
        # Determine card type from context
        card_type = "UNKNOWN"
        for brand in ["Amazon", "Apple", "Visa", "Xbox", "PlayStation", "Starbucks"]:
            if brand.lower() in context_text.lower():
                card_type = brand.upper()
                break

        try:
            with db._get_connection() as conn:
                conn.execute("""
                    INSERT INTO gift_card_vault (portal, card_type, card_code, value_usd, created_at)
                    VALUES ('GMAIL_HARVEST', ?, ?, ?, ?)
                """, (card_type, code, 25.0, time.time())) # Defaulting to $25 if not found
                conn.commit()
                return True
        except:
            return False # Duplicate code

code_harvester = GmailCodeHarvester()

if __name__ == "__main__":
    asyncio.run(code_harvester.harvest_codes_from_inbox(headless=True))
