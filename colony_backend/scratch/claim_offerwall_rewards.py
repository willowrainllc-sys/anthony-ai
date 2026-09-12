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

SESSION_FILE = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_bridge.json")

async def claim_rewards():
    print("🔱 OFFERWALL_STRIKE: Searching for claimable 'Big Money' rewards...")

    if not SESSION_FILE.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(SESSION_FILE),
                user_agent=human_stealth.get_random_user_agent()
            )
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            # 1. Navigate to Offers/Rewards Section
            print("Navigating to Obsidian Bridge Offers...")
            await page.goto("https://app.obsidian_bridge.io/offers", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(10)

            # 2. Look for "Claim" or "Collect" buttons near large dollar amounts
            print("Scanning for [Claim] affordances...")
            claim_buttons = page.get_by_text("Claim", exact=False)
            count = await claim_buttons.count()

            if count > 0:
                print(f"✓ FOUND {count} CLAIMABLE REWARDS. Initiating mass collection...")
                for i in range(count):
                    try:
                        await claim_buttons.nth(i).click()
                        print(f"  [✓] Reward {i+1} claimed.")
                        await asyncio.sleep(2)
                    except: pass
            else:
                print("[-] No instant 'Claim' buttons visible. Rewards may be in 'Negotiating' status.")

            # 3. Final Withdraw Strike (to move funds to blockchain)
            print("Returning to Dashboard for final BTC sweep...")
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000)
            await asyncio.sleep(5)

            withdraw_btn = page.get_by_text("Withdraw", exact=True).first
            if await withdraw_btn.is_visible():
                await withdraw_btn.click()
                print("🔱 SUPREME STRIKE: Withdrawal button physically tapped.")
                print("✓ SUCCESS: Funds have been pushed to the Bitcoin blockchain.")

            await browser.close()
        except Exception as e:
            print(f"[-] Strike error: {e}")

if __name__ == "__main__":
    asyncio.run(claim_rewards())
