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

HG_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_ingress.json")

async def force_transfer():
    print("🔱 OBSIDIAN_INGRESS_STRIKE: Initiating transfer to Obsidian Bridge...")

    if not HG_SESSION.exists():
        print("Error: No Obsidian Ingress session keys.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(HG_SESSION))
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            # 1. Access Obsidian Ingress
            print("Navigating to Obsidian Ingress Dashboard...")
            await page.goto("https://dashboard.obsidian_ingress.com/", timeout=60000)
            await asyncio.sleep(10)

            # 2. Look for the "Transfer to Obsidian Bridge" or JMPT Toggle
            print("Searching for JMPT Toggle/Transfer...")

            # Check if JMPT mode is already on
            is_jmpt = await page.get_by_text("Obsidian Bridge", exact=False).count() > 0
            print(f"JMPT Mentions found: {is_jmpt}")

            # Attempt to click the big yellow button if balance > $20
            # or the 'Transfer' link
            await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\hg_transfer_check.png")

            await browser.close()
            print("✓ Scan Complete. Proof saved to D: drive.")
        except Exception as e:
            print(f"[-] Strike error: {e}")

if __name__ == "__main__":
    asyncio.run(force_transfer())
