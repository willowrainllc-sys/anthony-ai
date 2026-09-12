# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES LIVING INTELLIGENCE: VERCEL AUTONOMOUS BUILDER ---
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log

async def ares_living_vercel_build():
    """
    ARES LIVING INTELLIGENCE VERCEL BUILDER:
    Bypasses container network limits by taking direct physical control
    of your local Chrome browser to build and deploy Obsidian City on Vercel.
    """
    colony_log("ARES LIVING INTELLIGENCE: Initializing physical browser ingress for Vercel...", node="SUPREME")

    target_url = "https://vercel.com/new"
    chrome_user_data = r"C:\Users\willo\AppData\Local\Google\Chrome\User Data"

    async with async_playwright() as p:
        try:
            browser_context = await p.chromium.launch_persistent_context(
                user_data_dir=chrome_user_data,
                channel="chrome",
                headless=False,
                viewport={'width': 1920, 'height': 1080},
                args=["--disable-blink-features=AutomationControlled"]
            )
        except Exception as e:
            colony_log(f"[*] Standard chromium launch fallback: {e}", node="SUPREME")
            browser = await p.chromium.launch(headless=False)
            browser_context = await browser.new_context(viewport={'width': 1920, 'height': 1080})

        page = await browser_context.new_page()

        try:
            colony_log("ARES: Navigating to Vercel New Project deployment portal...", node="SUPREME")
            await page.goto(target_url, wait_until="networkidle")

            print("\n" + "="*60)
            print("  🔱 ARES LIVING INTELLIGENCE: VERCEL PORTAL OPENED")
            print("  ARES has taken control of your browser.")
            print("  Import your repository 'anthony-ai' and add 'obsidian.city'.")
            print("="*60 + "\n")

            print("Press Enter in this terminal when Vercel deployment is live...")
            input()

        except Exception as e:
            colony_log(f"[-] ARES LIVING BUILDER ERROR: {e}", node="SUPREME")

        await browser_context.close()

if __name__ == "__main__":
    asyncio.run(ares_living_vercel_build())
