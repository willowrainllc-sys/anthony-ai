# --- WILLOW RAIN SECURITY: CHROME COOKIE SNIPER v1.0 ---
import asyncio
import os
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from human_stealth_helper import human_stealth

CHROME_PROFILE = Path(r"C:\Users\willo\AppData\Local\Google\Chrome\User Data")
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
JMPT_AUTH = PERSONA_VAULT / "obsidian_bridge_auth.json"

async def snipe():
    print(f"🔱 COOKIE_SNIPER: Attempting to piggyback on Chrome profile...")

    async with async_playwright() as p:
        try:
            # We use 'launch_persistent_context' to use the real Chrome data
            # Note: This will FAIL if Chrome is currently open.
            context = await p.chromium.launch_persistent_context(
                user_data_dir=str(CHROME_PROFILE),
                channel="chrome", # Use the actual Chrome installation
                headless=True,
                user_agent=human_stealth.get_random_user_agent(),
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()

            print("Navigating to Obsidian Bridge...")
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(5)

            # Check if we are logged in
            content = await page.evaluate("() => document.body.innerText")
            if "Withdraw" in content or "Dashboard" in content:
                print("✓ SUCCESS: Piggyback successful. Capturing session...")
                state = await context.storage_state()
                with open(JMPT_AUTH, 'w') as f:
                    json.dump(state, f, indent=4)
                print(f"Vaulted Obsidian Bridge session to {JMPT_AUTH}")
            else:
                print(f"[-] Failed. Content doesn't look like a dashboard. URL: {page.url}")
                await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\sniper_fail.png")

            await context.close()
        except Exception as e:
            print(f"[-] Sniper Error: {e}")
            print("NOTE: This tool fails if Chrome is currently running. Close all Chrome windows and retry.")

if __name__ == "__main__":
    asyncio.run(snipe())
