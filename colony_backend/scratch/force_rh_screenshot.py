import asyncio
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(sys_path)

from human_stealth_helper import human_stealth
from playwright_stealth_factory import stealth_factory

SESSION_FILE = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_robinhood.json")

async def take_shot():
    if not SESSION_FILE.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(SESSION_FILE),
                user_agent=human_stealth.get_random_user_agent(),
                viewport={'width': 1280, 'height': 2000}
            )
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            print("Navigating to Robinhood Portfolio...")
            await page.goto("https://robinhood.com/account/investing", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(15)

            shot_path = r"D:\ObsidianAi_Swarm\Temp\RH_REAL_TRUTH.png"
            await page.screenshot(path=shot_path, full_page=True)
            print(f"🔱 SUPREME PROOF SAVED TO: {shot_path}")

            await browser.close()
        except Exception as e:
            print(f"[-] Shot error: {e}")

if __name__ == "__main__":
    asyncio.run(take_shot())
