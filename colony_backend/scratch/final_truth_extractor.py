import asyncio
import os
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(sys_path)

from human_stealth_helper import human_stealth
from playwright_stealth_factory import stealth_factory

JMPT_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_bridge.json")

async def extract():
    print("🔱 TRUTH_EXTRACTOR: Reading live transaction history...")

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(JMPT_SESSION))
            page = await context.new_page()

            await page.goto("https://app.obsidian_bridge.io/transactions", timeout=60000)
            await asyncio.sleep(8)

            # Scrape transaction table
            rows = await page.locator("tr").all()
            print(f"\n--- OBSIDIAN_BRIDGE TRANSACTION HISTORY ({len(rows)} entries) ---")
            for i, row in enumerate(rows[:10]):
                text = await row.inner_text()
                print(f" [{i}] {text.replace('\n', ' | ')}")

            # Check Dashboard Balance
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000)
            await asyncio.sleep(5)
            content = await page.evaluate("() => document.body.innerText")
            print(f"\n--- DASHBOARD STATUS ---")
            if "Withdraw" in content:
                print("[!] Withdraw button is VISIBLE.")

            # Look for the 'Available' amount specifically
            avail_matches = re.findall(r'Available.*?\$([0-9.]+)', content, re.IGNORECASE)
            print(f"Available for Withdrawal: {avail_matches}")

            await browser.close()
        except Exception as e:
            print(f"[-] Extraction Error: {e}")

if __name__ == "__main__":
    asyncio.run(extract())
