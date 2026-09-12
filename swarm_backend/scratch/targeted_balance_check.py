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

async def check():
    if not JMPT_SESSION.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(JMPT_SESSION), user_agent=human_stealth.get_random_user_agent())
        page = await context.new_page()
        await human_stealth.inject_stealth_scripts(page)

        print("Navigating to Obsidian Bridge Dashboard...")
        await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
        await asyncio.sleep(10)

        # 1. Total Balance (The Big Number)
        total_balance = await page.locator("div:has-text('Total Balance') + div").first.inner_text() if await page.locator("div:has-text('Total Balance')").count() > 0 else "N/A"

        # 2. Available for Withdrawal
        available = await page.locator("span:has-text('Available')").first.inner_text() if await page.locator("span:has-text('Available')").count() > 0 else "N/A"

        # 3. Obsidian Ingress Specific Box
        # We search for the Obsidian Ingress card/box
        hg_card = page.locator("div:has-text('Obsidian Ingress')").first
        hg_text = await hg_card.inner_text() if await hg_card.count() > 0 else "N/A"

        print("\n=== 🔱 TARGETED OBSIDIAN_BRIDGE AUDIT ===")
        print(f"  TOTAL BALANCE: {total_balance}")
        print(f"  AVAILABLE:     {available}")
        print(f"  OBSIDIAN_INGRESS BOX: {hg_text.splitlines()[:5]}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check())
