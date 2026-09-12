# --- WILLOW RAIN SECURITY: OBSIDIAN HEADED HANDSHAKE v1.0 ---
import asyncio
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright

# Emulate the phone environment precisely
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
JMPT_AUTH = PERSONA_VAULT / "cookie_monster" / "cookie_monster_obsidian_bridge.json"

async def open_headed_phone_browser():
    """
    Opens a VISIBLE browser window emulating your phone.
    Log in manually here, and I will capture the cookies for the 9k strike.
    """
    print("[SUPREME] HEADED_HANDSHAKE: Opening visible phone-emulated portal...")

    async with async_playwright() as p:
        # Use Pixel 7 specs
        device = p.devices['Pixel 7']

        # Launch VISIBLE (headed=True)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(**device)
        page = await context.new_page()

        print("\n[!] ACTION REQUIRED: Log in to ObsidianBridge in the browser window.")
        print("[!] Ensure you see the $0.06 balance.")
        print("[!] Once logged in, CLOSE THE BROWSER window to save session.")

        await page.goto("https://app.obsidian_bridge.io/login", timeout=0)

        # Wait for the user to close the window
        while not browser.is_connected():
            await asyncio.sleep(1)

        # Capture and vault
        state = await context.storage_state()
        with open(JMPT_AUTH, 'w') as f:
            json.dump(state, f, indent=4)

        print(f" SUCCESS: Physical session captured and vaulted to {JMPT_AUTH}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(open_headed_phone_browser())
