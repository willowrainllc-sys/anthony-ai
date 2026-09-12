import asyncio
import os
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from human_stealth_helper import human_stealth

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
GMAIL_FILE = PERSONA_VAULT / "cookie_monster" / "cookie_monster_gmail.json"
JMPT_AUTH = PERSONA_VAULT / "obsidian_bridge_auth.json"

async def attempt():
    if not GMAIL_FILE.exists():
        print("Error: No Gmail session.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            storage_state=str(GMAIL_FILE),
            user_agent=human_stealth.get_random_user_agent(),
            viewport={'width': 1280, 'height': 800}
        )
        page = await context.new_page()
        await human_stealth.inject_stealth_scripts(page)

        print("Navigating to Obsidian Bridge...")
        await page.goto("https://obsidian_bridge.io/", timeout=60000)
        await asyncio.sleep(5)

        # Click Login
        try:
            await page.get_by_role("link", name="Log in").click()
            await asyncio.sleep(5)

            # Click Login with Google
            # Note: This often opens a popup or redirects
            print("Attempting to click 'Continue with Google'...")
            google_btn = page.get_by_role("button", name="Continue with Google").first
            if await google_btn.is_visible():
                await google_btn.click()
                await asyncio.sleep(10)

            # Check if we landed in the dashboard
            if "app.obsidian_bridge.io/dashboard" in page.url or await page.get_by_text("Withdraw").count() > 0:
                print("✓ SUCCESS: Logged in to Obsidian Bridge via Google session.")
                state = await context.storage_state()
                with open(JMPT_AUTH, 'w') as f:
                    json.dump(state, f, indent=4)
                print(f"Vaulted new Obsidian Bridge session to {JMPT_AUTH}")
            else:
                print(f"[-] Failed. Current URL: {page.url}")
                await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\obsidian_bridge_login_fail.png")

        except Exception as e:
            print(f"Error during login: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(attempt())
