# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES VERCEL MAGIC LINK AUTHENTICATOR ---
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log

async def ares_vercel_magic_link():
    """
    ARES VERCEL MAGIC LINK AUTHENTICATOR:
    Bypasses Google OAuth blocks entirely by requesting and authenticating
    via Vercel Email Magic Link.
    """
    colony_log("ARES VERCEL MAGIC LINK: Initiating secure email sign-in...", node="SUPREME")

    profile_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\ares_browser_profile")
    profile_dir.mkdir(parents=True, exist_ok=True)

    target_url = "https://vercel.com/login"

    async with async_playwright() as p:
        browser_context = await p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            args=["--disable-blink-features=AutomationControlled"]
        )
        page = await browser_context.new_page()

        try:
            colony_log("ARES: Navigating to Vercel login portal...", node="SUPREME")
            await page.goto(target_url, wait_until="networkidle")

            print("\n" + "="*70)
            print("  🔱 ARES VERCEL MAGIC LINK AUTHENTICATOR ACTIVE")
            print("  1. Enter your email in the opened browser window.")
            print("  2. Click 'Continue with Email' to receive your Vercel Magic Link.")
            print("  3. Click the Magic Link in your email to log in.")
            print("="*70 + "\n")

            # Wait until user reaches Vercel dashboard after clicking magic link
            await page.wait_for_url("https://vercel.com/dashboard", timeout=300000)
            colony_log("✓ ARES SUCCESS: Vercel session authenticated via Magic Link and vaulted!", node="SUPREME")

        except Exception as e:
            colony_log(f"[-] VERCEL MAGIC LINK NOTICE: {e}", node="SUPREME")

        await browser_context.close()

if __name__ == "__main__":
    asyncio.run(ares_vercel_magic_link())
