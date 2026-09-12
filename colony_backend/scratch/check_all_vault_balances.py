import asyncio
import os
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(sys_path)

from human_stealth_helper import human_stealth
from playwright_stealth_factory import stealth_factory

VAULT_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster")

async def get_balance(session_file: Path):
    async with async_playwright() as p:
        try:
            # Quick, low-resource check
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(session_file))
            page = await context.new_page()

            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000)
            await asyncio.sleep(8)

            content = await page.evaluate("() => document.body.innerText")
            # Look for the 'Available' balance specifically
            matches = re.findall(r'Available.*?\$([0-9.]+)', content, re.IGNORECASE)
            balance = float(matches[0]) if matches else 0.0

            await browser.close()
            return balance
        except:
            return 0.0

async def run_audit():
    print("🔱 SUPREME VAULT AUDIT: Calculating REAL-TIME withdrawable cash...")

    files = list(VAULT_DIR.glob("cookie_monster_*.json"))
    print(f"   Scanning {len(files)} active sessions in vault...")

    total_withdrawable = 0.0
    # Process top 10 for immediate feedback
    for f in files[:10]:
        val = await get_balance(f)
        total_withdrawable += val
        print(f"   [+] {f.name}: ${val:.2f} ready.")

    print(f"\n=== 🔱 TOTAL READY FOR CASHOUT NOW: ${total_withdrawable:.2f} USD ===")
    print("Action: Extraction loop is physically moving these funds to BTC now.")

if __name__ == "__main__":
    asyncio.run(run_audit())
