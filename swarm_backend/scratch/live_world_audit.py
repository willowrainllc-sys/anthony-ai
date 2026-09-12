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

JMPT_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_bridge.json")
RH_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_robinhood.json")

async def take_screenshot(session_file, url, name):
    if not session_file.exists():
        print(f"[-] {name}: No session file.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(session_file),
                user_agent=human_stealth.get_random_user_agent(),
                viewport={'width': 1280, 'height': 1200}
            )
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            print(f"Navigating to {name} ({url})...")
            await page.goto(url, timeout=60000, wait_until="networkidle")
            await asyncio.sleep(10)

            shot_path = f"D:\\ObsidianAi_Swarm\\Temp\\LIVE_AUDIT_{name.upper()}.png"
            await page.screenshot(path=shot_path, full_page=True)
            print(f"[✓] {name} PROOF: {shot_path}")

            await browser.close()
        except Exception as e:
            print(f"[-] {name} Error: {e}")

async def run():
    print("=== 🔱 SUPREME LIVE WORLD AUDIT: NO LIES ===\n")
    # Audit Robinhood History
    await take_screenshot(RH_SESSION, "https://robinhood.com/account/history", "ROBINHOOD_HISTORY")
    # Audit Obsidian Bridge History
    await take_screenshot(JMPT_SESSION, "https://app.obsidian_bridge.io/transactions", "OBSIDIAN_BRIDGE_HISTORY")

if __name__ == "__main__":
    asyncio.run(run())
