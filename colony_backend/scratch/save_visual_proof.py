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

async def save_proof():
    if not JMPT_SESSION.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            # We use a large viewport to see EVERYTHING
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(JMPT_SESSION),
                user_agent=human_stealth.get_random_user_agent(),
                viewport={'width': 1920, 'height': 2000}
            )
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            print("Navigating to Obsidian Bridge Dashboard for Full Proof...")
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(15) # Long wait for all widgets to load

            # Capture a massive screenshot of the full dashboard
            proof_path = r"D:\ObsidianAi_Swarm\Temp\REAL_WORLD_PROOF_DIRECTOR_MAESTAS.png"
            await page.screenshot(path=proof_path, full_page=True)

            print(f"\n🔱 SUPREME PROOF SAVED TO: {proof_path}")
            print("Director, please open this file on your D: drive to see exactly what I see.")

            await browser.close()
        except Exception as e:
            print(f"[-] Proof error: {e}")

if __name__ == "__main__":
    asyncio.run(save_proof())
