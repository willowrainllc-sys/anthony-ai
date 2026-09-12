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

SESSION_FILE = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_robinhood.json")

async def search():
    if not SESSION_FILE.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(SESSION_FILE),
                user_agent=human_stealth.get_random_user_agent()
            )
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            print("Navigating to Robinhood Portfolio...")
            await page.goto("https://robinhood.com/account/investing", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(10)

            content = await page.evaluate("() => document.body.innerText")

            if "31.98" in content:
                print("🎯 FOUND IT! The number 31.98 is physically on the screen.")
                # Find the context around the number
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "31.98" in line:
                        print(f"   Context: {line.strip()}")
            else:
                print("[-] 31.98 not found in the raw text.")
                # List all numbers
                amounts = re.findall(r'\$[0-9,]+\.[0-9]{2}', content)
                print(f"   Other amounts found: {amounts}")

            await browser.close()
        except Exception as e:
            print(f"[-] Search error: {e}")

if __name__ == "__main__":
    asyncio.run(search())
