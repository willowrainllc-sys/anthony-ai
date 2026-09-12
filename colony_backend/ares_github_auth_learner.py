# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES GITHUB AUTHENTICATION & SESSION LEARNER ---
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log

async def ares_github_learner():
    """
    ARES GITHUB AUTHENTICATION LEARNER:
    Opens GitHub in headed mode so the Director can securely log in,
    update passwords, and authenticate. ARES records and vaults the session
    for 100% automated GitHub & Vercel deployments.
    """
    colony_log("ARES GITHUB LEARNER: Opening secure browser for GitHub authentication...", node="SUPREME")

    profile_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\ares_browser_profile")
    profile_dir.mkdir(parents=True, exist_ok=True)

    target_url = "https://github.com/login"

    async with async_playwright() as p:
        browser_context = await p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = await browser_context.new_page()

        try:
            colony_log("ARES: Navigating to GitHub login...", node="SUPREME")
            await page.goto(target_url, wait_until="networkidle")

            print("\n" + "="*70)
            print("  🔱 ARES GITHUB AUTHENTICATION LEARNER ACTIVE")
            print("  Please log in to your GitHub account (or update your password)")
            print("  in the opened browser window.")
            print("="*70 + "\n")

            # Wait until user reaches their GitHub dashboard or profile
            await page.wait_for_url("https://github.com/", timeout=300000)
            colony_log("✓ ARES SUCCESS: GitHub session successfully authenticated and learned!", node="SUPREME")

        except Exception as e:
            colony_log(f"[-] GITHUB LEARNER NOTICE: {e}", node="SUPREME")

        await browser_context.close()

if __name__ == "__main__":
    asyncio.run(ares_github_learner())
