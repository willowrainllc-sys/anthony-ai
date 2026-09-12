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

JMPT_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_bridge.json")

async def troubleshoot():
    print("🔱 PAYOUT_TROUBLESHOOT: Starting high-aura audit...")

    if not JMPT_SESSION.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(JMPT_SESSION), user_agent=human_stealth.get_random_user_agent())
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            # 1. Check for 'Suspended' or 'Flagged' messages
            print("   -> Scanning Dashboard for Red Flags...")
            await page.goto("https://dashboard.obsidian_ingress.com/", timeout=60000)
            await asyncio.sleep(10)

            content = await page.evaluate("() => document.body.innerText")
            if "suspended" in content.lower() or "blocked" in content.lower():
                print("   [!] ALERT: Dashboard shows a SUSPENSION/BLOCK message.")
            else:
                print("   [✓] NO FLAGS: Dashboard looks clean.")

            # 2. Count Active Devices
            # Looking for "Active devices" text and the number next to it
            try:
                device_count = await page.locator("div:has-text('Active devices') + div").inner_text()
                print(f"   [✓] ACTIVE DEVICES: {device_count}")
            except:
                # Scrape all text and find the line
                lines = content.split('\n')
                for line in lines:
                    if "Active devices" in line:
                        print(f"   [✓] DEVICE STATUS: {line.strip()}")

            # 3. Check Obsidian Bridge Connectivity
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000)
            await asyncio.sleep(10)

            # Look for the wallet address bc1qk4...
            jmpt_content = await page.content()
            if "bc1qk4ass5xsanvth2tz7jsapscy8ld25yr6ze5yzx" in jmpt_content:
                print("   [✓] WALLET SYNC: Correct BTC wallet is bound to JMPT.")
            else:
                print("   [!] WALLET ERROR: Your BTC wallet is NOT detected on the dashboard.")

            await browser.close()
        except Exception as e:
            print(f"[-] Troubleshooting error: {e}")

if __name__ == "__main__":
    asyncio.run(troubleshoot())
