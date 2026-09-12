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
HG_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_ingress.json")

async def take_proof(session_file, url, name):
    if not session_file.exists():
        print(f"[-] {name}: No session file.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(session_file),
                user_agent=human_stealth.get_random_user_agent(),
                viewport={'width': 1280, 'height': 800}
            )
            page = await context.new_page()

            print(f"Navigating to {name}...")
            await page.goto(url, timeout=60000, wait_until="networkidle")
            await asyncio.sleep(10)

            # Save screenshot for Director to verify
            shot_path = f"D:\\ObsidianAi_Swarm\\Temp\\proof_{name.lower()}.png"
            await page.screenshot(path=shot_path, full_page=True)
            print(f"[✓] {name} Screenshot saved to: {shot_path}")

            # Scrape critical text
            content = await page.evaluate("() => document.body.innerText")
            print(f"--- {name} CRITICAL DATA ---")
            for line in content.split('\n'):
                if '$' in line or 'Credits' in line or 'JMPT' in line:
                    if len(line.strip()) < 100:
                        print(f"  > {line.strip()}")

            await browser.close()
        except Exception as e:
            print(f"[-] {name} Error: {e}")

async def run():
    print("=== 🔱 SUPREME VISUAL PROOF AUDIT ===\n")
    await take_proof(HG_SESSION, "https://dashboard.obsidian_ingress.com/", "OBSIDIAN_INGRESS")
    print("-" * 30)
    await take_proof(JMPT_SESSION, "https://app.obsidian_bridge.io/dashboard", "OBSIDIAN_BRIDGE")

if __name__ == "__main__":
    asyncio.run(run())
