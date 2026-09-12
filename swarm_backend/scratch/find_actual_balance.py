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

async def search_for_067():
    print("🔱 BALANCE_SCAN: Hunting for the REAL $0.67 balance...")

    if not JMPT_SESSION.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            # We use a large window to make sure nothing is hidden
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(JMPT_SESSION),
                user_agent=human_stealth.get_random_user_agent(),
                viewport={'width': 1920, 'height': 1080}
            )
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            # 1. Check Obsidian Bridge Dashboard
            print("   -> Scanning Obsidian Bridge...")
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(10)

            content = await page.evaluate("() => document.body.innerText")

            if "0.67" in content:
                print("🎯 FOUND IT! $0.67 is physically on the Obsidian Bridge dashboard.")
                # Save proof
                await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\FOUND_067.png")
            else:
                print("[-] 0.67 not found on main dashboard.")
                # Check for "Total" or other wallets
                amounts = re.findall(r'\$[0-9,]+\.[0-9]{2}', content)
                print(f"   Other balances on screen: {amounts}")

            # 2. Check Obsidian Ingress Dashboard (for the 0.06)
            print("\n   -> Scanning Obsidian Ingress Standard...")
            await page.goto("https://dashboard.obsidian_ingress.com/", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(10)
            hg_content = await page.evaluate("() => document.body.innerText")

            if "0.06" in hg_content:
                print("🎯 FOUND IT! $0.06 is physically on the Obsidian Ingress dashboard.")
            else:
                print("[-] 0.06 not found on Obsidian Ingress dashboard.")

            await browser.close()
        except Exception as e:
            print(f"[-] Scan error: {e}")

if __name__ == "__main__":
    asyncio.run(search_for_067())
