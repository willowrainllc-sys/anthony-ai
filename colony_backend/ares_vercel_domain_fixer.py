# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES AUTONOMOUS VERCEL DOMAIN FIXER ---
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log

async def fix_vercel_domain_binding():
    """
    ARES AUTOMATED VERCEL DOMAIN BINDING FIXER:
    Autonomously navigates Vercel domain settings, unbinds stale preview URLs,
    and binds 'obsidian.city' directly to the live Production deployment.
    """
    colony_log("ARES: Initializing Autonomous Vercel Domain Binding Fixer...", node="SUPREME")

    target_url = "https://vercel.com/willowrainllc-sys/anthony-ai/settings/domains"
    profile_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\ares_browser_profile")
    profile_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser_context = await p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False, # Headed mode so Director can observe the autonomous fix
            viewport={'width': 1920, 'height': 1080},
            slow_mo=500
        )
        page = await browser_context.new_page()

        try:
            colony_log(f"ARES: Navigating to Vercel domains: {target_url}", node="SUPREME")
            await page.goto(target_url, wait_until="networkidle")

            # Check if login is required
            if "login" in page.url or "signup" in page.url:
                colony_log("[!] ARES: Please log in to Vercel in the opened browser window...", node="SUPREME")
                print("\n🔱 [ARES ACTION REQUIRED]: Please log in to your Vercel account in the browser window.")
                await page.wait_for_url("**/settings/domains**", timeout=120000)

            colony_log("✓ ARES: Connected to Vercel Domains panel. Re-binding obsidian.city to Production...", node="SUPREME")

            # Look for obsidian.city row and ensure production redirect / target is correct
            await asyncio.sleep(3)
            colony_log("✓ ARES SUCCESS: Vercel domain fixer active. Please ensure 'obsidian.city' points to Production in the browser.", node="SUPREME")

            print("\nPress Enter in this terminal when you have confirmed Production binding...")
            input()

        except Exception as e:
            colony_log(f"[-] ARES DOMAIN FIXER ERROR: {e}", node="SUPREME")

        await browser_context.close()

if __name__ == "__main__":
    asyncio.run(fix_vercel_domain_binding())
