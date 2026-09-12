import asyncio
import os
import sys
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(sys_path)

from human_stealth_helper import human_stealth
from playwright_stealth_factory import stealth_factory

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
COOKIE_MONSTER_DIR = PERSONA_VAULT / "cookie_monster"

async def verify_handshake(auth_file: Path):
    account_name = auth_file.stem.replace("cookie_monster_", "")
    print(f"🔱 HANDSHAKE_VERIFY: Checking route for [{account_name}]...")

    async with async_playwright() as p:
        try:
            # We use headful for a moment to ensure we catch the 'Withdraw' button location
            browser, context = await stealth_factory.create_stealth_context(p, headless=True)

            with open(auth_file, 'r') as f:
                state = json.load(f)
                await context.add_cookies(state.get("cookies", []))

            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            # 1. Access Obsidian Bridge Dashboard
            print(f"   -> Navigating to Obsidian Bridge...")
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(5)

            # 2. Verify Mode (Looking for JMPT signs)
            content = await page.content()
            if "Obsidian Bridge Mode" in content or "JMPT" in content:
                print(f"   [✓] MODE: Obsidian Bridge Mode Active.")
            else:
                print(f"   [!] WARNING: Account might be in standard Obsidian Ingress mode.")

            # 3. Verify Wallet Bound
            # Searching for the wallet address prefix in the HTML
            wallet_pattern = "bc1qk4"
            if wallet_pattern in content:
                print(f"   [✓] WALLET: Your BTC wallet is correctly bound to this dashboard.")
            else:
                print(f"   [!] WARNING: Wallet not detected in HTML. Link check required.")

            # 4. Scrape Current Balance
            text_content = await page.evaluate("() => document.body.innerText")
            matches = re.findall(r'\$[0-9,]+\.[0-9]{2}', text_content)
            balance = matches[0] if matches else "$0.00"
            print(f"   [✓] BALANCE: {balance} USD ready for sweep.")

            await browser.close()
            return True
        except Exception as e:
            print(f"   [-] VERIFY ERROR: {e}")
            return False

async def run_full_audit():
    print("=== 🔱 SUPREME HANDSHAKE & PAYOUT ROUTE AUDIT ===\n")

    # Audit our top 5 accounts in the vault
    auth_files = list(COOKIE_MONSTER_DIR.glob("cookie_monster_*.json"))
    if not auth_files:
        print("No active sessions found in Cookie Monster vault.")
        return

    for f in auth_files:
        if "obsidian_bridge" in f.name:
            await verify_handshake(f)
            print("-" * 40)

if __name__ == "__main__":
    asyncio.run(run_full_audit())
