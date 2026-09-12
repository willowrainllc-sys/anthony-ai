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

VAULT_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster")

async def check_balance(session_file: Path):
    print(f"🔱 AUDITING: {session_file.name}...")

    async with async_playwright() as p:
        try:
            browser, context = await stealth_factory.create_stealth_context(p, headless=True)
            with open(session_file, 'r') as f:
                state = json.load(f)
                await context.add_cookies(state.get("cookies", []))

            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            # Obsidian Bridge Check
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(5)

            content = await page.evaluate("() => document.body.innerText")
            matches = re.findall(r'\$[0-9,]+\.[0-9]{2}', content)

            if matches:
                print(f"   Balances: {matches}")
                if any(m == "$0.06" for m in matches):
                    print(f"🎯 FOUND IT! Account in {session_file.name} has $0.06.")
                    return True

            await browser.close()
        except Exception as e:
            print(f"   [-] Error on {session_file.name}: {e}")
        return False

async def run_search():
    print("=== 🔱 SEARCHING FOR THE REAL $0.06 ACCOUNT ===\n")

    # List all possible cookie files
    files = list(VAULT_DIR.glob("*.json"))

    for f in files:
        if await check_balance(f):
            print(f"\n[✓] SUCCESS: Verified account with $0.06 found in {f.name}")
            break
        print("-" * 30)

if __name__ == "__main__":
    asyncio.run(run_search())
