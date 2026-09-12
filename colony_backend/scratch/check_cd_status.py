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
HG_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_ingress.json")

async def check_cd(session_file, name):
    if not session_file.exists():
        return f"[-] {name}: No session file."

    async with async_playwright() as p:
        try:
            browser, context = await stealth_factory.create_stealth_context(p, headless=True)
            with open(session_file, 'r') as f:
                state = json.load(f)
                await context.add_cookies(state.get("cookies", []))

            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            print(f"🔱 AUDITING {name} FOR CONTENT DELIVERY...")
            await page.goto("https://dashboard.obsidian_ingress.com/", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(8)

            content = await page.evaluate("() => document.body.innerText")

            # Check for CD keywords
            cd_status = "NOT_FOUND"
            if "Content Delivery" in content:
                if "Active" in content: cd_status = "ACTIVE (6 cr/hr)"
                elif "Queue" in content: cd_status = "IN_QUEUE"
                else: cd_status = "AVAILABLE"

            await browser.close()
            return f"[✓] {name} CD STATUS: {cd_status}"
        except Exception as e:
            return f"[-] {name} Error: {e}"

async def run():
    print("=== 🔱 SUPREME CONTENT DELIVERY AUDIT ===\n")
    # Audit Obsidian Ingress Master
    res = await check_cd(HG_SESSION, "OBSIDIAN_INGRESS_MASTER")
    print(res)

if __name__ == "__main__":
    asyncio.run(run())
