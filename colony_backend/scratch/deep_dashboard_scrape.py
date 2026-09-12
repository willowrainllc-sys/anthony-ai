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

async def scrape():
    if not JMPT_SESSION.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(storage_state=str(JMPT_SESSION), user_agent=human_stealth.get_random_user_agent())
        page = await context.new_page()
        await human_stealth.inject_stealth_scripts(page)

        print("Navigating to Obsidian Bridge Dashboard...")
        await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
        await asyncio.sleep(10)

        # Scrape every single piece of text on the page and group by parent div
        data = await page.evaluate("""() => {
            const results = [];
            document.querySelectorAll('div').forEach(div => {
                if (div.innerText && div.innerText.includes('$') && div.children.length < 5) {
                    results.push(div.innerText.replace(/\n/g, ' '));
                }
            });
            return results;
        }""")

        print("\n=== 🔱 DEEP OBSIDIAN_BRIDGE SCRAPE ===")
        for d in set(data): # Use set to remove duplicates
            if len(d) < 100:
                print(f" [DATA] {d}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape())
