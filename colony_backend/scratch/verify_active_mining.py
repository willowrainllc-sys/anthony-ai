import asyncio
import os
import sys
import json
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(sys_path)

from human_stealth_helper import human_stealth
from playwright_stealth_factory import stealth_factory

JMPT_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_bridge.json")

async def verify():
    print("🔱 MINING_VERIFY: Checking live node activity and $0.67 balance...")

    if not JMPT_SESSION.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(JMPT_SESSION), user_agent=human_stealth.get_random_user_agent())
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            # 1. Dashboard Check
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(10)

            content = await page.evaluate("() => document.body.innerText")

            print("\n--- REAL-WORLD DASHBOARD DATA ---")
            if "0.67" in content:
                print("🎯 VERIFIED: Found the $0.67 balance. The Director is correct.")
            else:
                print(f"[-] Discrepancy: Physically found different values on screen.")

            # 2. Device/Node Audit (Looking for Obsidian Ingress connected devices)
            try:
                # Navigating to the linked devices section
                await page.goto("https://dashboard.obsidian_ingress.com/", timeout=60000)
                await asyncio.sleep(10)
                hg_content = await page.evaluate("() => document.body.innerText")

                # Check for active devices count
                if "Active devices" in hg_content:
                    print(f"\n[✓] ACTIVE DEVICES DETECTED: Found device list in dashboard.")
                else:
                    print("\n[!] WARNING: No active devices list found. Nodes might be DISCONNECTED.")

            except: pass

            await browser.close()
        except Exception as e:
            print(f"[-] Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
