import asyncio
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(sys_path)

JMPT_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_bridge.json")

async def read():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(JMPT_SESSION))
        page = await context.new_page()

        await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000)
        await asyncio.sleep(15)

        text = await page.evaluate("() => document.body.innerText")
        print("--- FULL DASHBOARD TEXT ---")
        print(text)
        print("--- END ---")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(read())
