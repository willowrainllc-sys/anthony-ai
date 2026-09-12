import asyncio
import os
import sys
from pathlib import Path
from playwright.async_api import async_playwright

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from human_stealth_helper import human_stealth

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
SESSION_FILE = PERSONA_VAULT / "cashapp_auth.json"

async def discover():
    if not SESSION_FILE.exists():
        print("Error: No session file.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(SESSION_FILE), user_agent=human_stealth.get_random_user_agent())
        page = await context.new_page()
        await human_stealth.inject_stealth_scripts(page)

        print("Navigating to Cash App account page...")
        await page.goto("https://cash.app/account", timeout=60000, wait_until="networkidle")
        await asyncio.sleep(10)

        await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\cashapp_dashboard.png")

        # List buttons and links
        elements = await page.evaluate("""() => {
            const items = [];
            document.querySelectorAll('button, a, span').forEach(el => {
                if (el.innerText.trim()) {
                    items.push({tag: el.tagName, text: el.innerText.trim()});
                }
            });
            return items;
        }""")

        print(f"Found {len(elements)} elements.")
        for i, el in enumerate(elements[:50]):
            print(f"[{i}] {el['tag']}: {el['text']}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(discover())
