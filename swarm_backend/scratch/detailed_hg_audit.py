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

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
HG_SESSION = PERSONA_VAULT / "cookie_monster" / "cookie_monster_obsidian_ingress.json"
JMPT_SESSION = PERSONA_VAULT / "cookie_monster" / "cookie_monster_obsidian_bridge.json"

async def audit_account(session_file, label, url):
    if not session_file.exists():
        print(f"[-] {label}: No session file.")
        return

    print(f"🔱 AUDITING {label}...")
    async with async_playwright() as p:
        try:
            browser, context = await stealth_factory.create_stealth_context(p, headless=True)
            with open(session_file, 'r') as f:
                state = json.load(f)
                await context.add_cookies(state.get("cookies", []))

            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            await page.goto(url, timeout=60000, wait_until="networkidle")
            await asyncio.sleep(8)

            content = await page.evaluate("() => document.body.innerText")

            # Find all dollar amounts
            matches = re.findall(r'\$[0-9,]+\.[0-9]{2}', content)
            print(f"   Balances found on {label} page:")
            for m in matches:
                print(f"    - {m}")

            await browser.close()
        except Exception as e:
            print(f"   [-] Error: {e}")

async def run():
    print("=== 🔱 DETAILED REAL-WORLD REVENUE AUDIT ===\n")
    # Audit Obsidian Ingress Dashboard (Standard Pot)
    await audit_account(HG_SESSION, "OBSIDIAN_INGRESS_DASHBOARD", "https://dashboard.obsidian_ingress.com/")
    print("-" * 30)
    # Audit Obsidian Bridge Dashboard (Crypto Pot)
    await audit_account(JMPT_SESSION, "OBSIDIAN_BRIDGE_DASHBOARD", "https://app.obsidian_bridge.io/dashboard")

if __name__ == "__main__":
    asyncio.run(run())
