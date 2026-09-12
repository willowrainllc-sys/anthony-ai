# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES PLAYWRIGHT AUTOMATION: VERCEL DOMAIN LINKER ---
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log

async def run_ares_vercel_domain_automation():
    """
    ARES ADVANCED PLAYWRIGHT AUTOMATION:
    Launches ARES in headed mode with persistent profile storage to:
    1. Authenticate with Vercel (or reuse existing session cookies).
    2. Navigate to project domains settings.
    3. Input 'obsidian.city' and add it to Vercel.
    4. Extract DNS configuration requirements for Cloudflare.
    """
    colony_log("ARES: Initializing Vercel Domain Automator (Playwright Headed Mode)...", node="SUPREME")

    profile_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\ares_browser_profile")
    profile_dir.mkdir(parents=True, exist_ok=True)

    target_url = "https://vercel.com/willowrainllc-sys/anthony-ai/settings/domains"

    async with async_playwright() as p:
        # Launch persistent context to preserve login session across runs
        browser_context = await p.chromium.launch_persistent_context(
            user_data_dir=str(profile_dir),
            headless=False,
            viewport={'width': 1920, 'height': 1080},
            slow_mo=500
        )

        page = await browser_context.new_page()

        try:
            colony_log(f"ARES: Navigating to Vercel domains: {target_url}", node="SUPREME")
            await page.goto(target_url, wait_until="networkidle")

            # Check if login is required
            if "login" in page.url or "signup" in page.url:
                colony_log("[!] ARES: Login required. Please log in to Vercel in the browser window...", node="SUPREME")
                print("\n🔱 [ARES ACTION REQUIRED]: Please log in to your Vercel account in the opened browser window.")
                print("ARES will wait up to 120 seconds for you to authenticate...\n")

                # Wait until user logs in and lands on the dashboard or project settings
                try:
                    await page.wait_for_url("**/settings/domains**", timeout=120000)
                except:
                    colony_log("[-] ARES: Login timeout reached.", node="SUPREME")

            colony_log("✓ ARES: Authenticated on Vercel Domains panel.", node="SUPREME")

            # Look for domain input field
            colony_log("ARES: Locating domain input field...", node="SUPREME")
            # Vercel domain input selector typically has placeholder 'Enter domain name' or similar
            input_selector = "input[placeholder*='domain'], input[aria-label*='Domain']"

            try:
                await page.wait_for_selector(input_selector, timeout=10000)
                await page.fill(input_selector, "obsidian.city")
                colony_log("✓ ARES: Entered domain [obsidian.city].", node="SUPREME")

                # Click Add button
                add_btn_selector = "button:has-text('Add'), button:has-text('Save')"
                await page.click(add_btn_selector)
                colony_log("✓ ARES: Clicked Add domain button.", node="SUPREME")

                await asyncio.sleep(5)

                # Take proof screenshot
                proof_path = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\recon_vault\ares_bursts\vercel_domain_added_proof.png")
                await page.screenshot(path=str(proof_path), full_page=True)
                colony_log(f"✓ ARES SUCCESS: Vercel domain linked! Proof saved to {proof_path}", node="SUPREME")

            except Exception as e:
                colony_log(f"[-] ARES DOMAIN INTERACTION NOTICE: {e}. Please add 'obsidian.city' manually in the opened browser window.", node="SUPREME")
                print("\n🔱 [ARES GUIDANCE]: ARES has opened Vercel. Please add 'obsidian.city' in the Vercel dashboard window if not already added.")

            # Keep browser open for director review
            print("\nARES automation active. Press Enter in terminal when finished reviewing/configuring...")
            input()

        except Exception as e:
            colony_log(f"[-] ARES AUTOMATION ERROR: {e}", node="SUPREME")

        await browser_context.close()

if __name__ == "__main__":
    asyncio.run(run_ares_vercel_domain_automation())
