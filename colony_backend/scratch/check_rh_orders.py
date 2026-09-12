import os
import sys
import json
import asyncio
from pathlib import Path
from playwright.async_api import async_playwright

# Add colony_backend to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from human_stealth_helper import human_stealth

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
SESSION_FILE = PERSONA_VAULT / "robinhood_auth.json"

async def check_orders():
    if not SESSION_FILE.exists():
        print("Error: No session file.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            storage_state=str(SESSION_FILE),
            user_agent=human_stealth.get_random_user_agent(),
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()
        await human_stealth.inject_stealth_scripts(page)

        print("Navigating to Robinhood History...")
        await page.goto("https://robinhood.com/account/history", timeout=60000, wait_until="networkidle")
        await asyncio.sleep(5)

        # Dump history text
        history_text = await page.evaluate("() => document.body.innerText")

        print("--- RECENT ROBINHOOD HISTORY ---")
        lines = history_text.split('\n')
        # Print top 30 lines of history to see recent activity
        for line in lines[:50]:
            if any(kw in line for kw in ["BTC", "Buy", "Market", "Limit", "Filled", "Queued"]):
                print(line)
        print("--- END ---")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(check_orders())
