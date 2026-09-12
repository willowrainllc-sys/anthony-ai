import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from human_stealth_helper import human_stealth

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
SESSION_FILE = PERSONA_VAULT / "robinhood_auth.json"

async def discover():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(SESSION_FILE), user_agent=human_stealth.get_random_user_agent())
        page = await context.new_page()
        await human_stealth.inject_stealth_scripts(page)

        print("Navigating to BTC page...")
        await page.goto("https://robinhood.com/crypto/BTC", timeout=60000, wait_until="networkidle")
        await asyncio.sleep(10)

        # Take a screenshot
        await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\rh_btc_page.png")

        # List buttons and inputs
        buttons = await page.locator("button").all()
        print(f"Found {len(buttons)} buttons.")
        for i, btn in enumerate(buttons):
            try:
                txt = await btn.inner_text()
                if txt:
                    print(f"Btn [{i}]: {txt.strip()}")
            except: pass

        inputs = await page.locator("input").all()
        print(f"Found {len(inputs)} inputs.")
        for i, inp in enumerate(inputs):
            try:
                placeholder = await inp.get_attribute("placeholder")
                print(f"Inp [{i}]: Placeholder='{placeholder}'")
            except: pass

        await browser.close()

if __name__ == "__main__":
    asyncio.run(discover())
