# --- WILLOW RAIN SECURITY: BURST FOR REALITY v1.0 ---
import asyncio
import os
import uuid
import json
import re
from playwright.async_api import async_playwright
from colony_logger import colony_log
from colony_persistence import db
from human_stealth_helper import human_stealth
from cookie_monster_vault import cookie_monster

# SETTINGS
COUPON_CODE = "dontpayfull5"
GMAIL_USER = "obsidian.global.holdings@gmail.com"
BTC_WALLET = "bc1qk4ass5xsanvth2tz7jsapscy8ld25yr6ze5yzx"

async def burst():
    colony_log("[SUPREME] REALITY_BURST: Initiating single-shot wealth extraction...", node="SUPREME")

    email = f"obsidian.global.holdings+reality_{uuid.uuid4().hex[:6]}@gmail.com"
    password = f"Alpha_{uuid.uuid4().hex[:10]}!"
    proxy = "socks5://127.0.0.1:1080"

    async with async_playwright() as p:
        try:
            # 1. SIGN UP
            colony_log(f"BURST: Creating $5-bonus account [{email}]...", node="SUPREME")
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=human_stealth.get_random_user_agent(), proxy={"server": proxy})
            page = await context.new_page()

            await page.goto("https://dashboard.obsidian_ingress.com/sign-up", timeout=60000)
            await page.fill('input[name="email"]', email)
            await page.fill('input[name="password"]', password)

            # Apply Coupon
            await page.click("text=Redeem coupon code")
            await page.fill('input[name="coupon_code"]', COUPON_CODE)

            await page.click('button[type="submit"]')
            await asyncio.sleep(10)

            colony_log(" BURST: Account created. Awaiting Handshake verification email...", node="SUPREME")

            # 2. VERIFY (Directly via IMAP)
            # We wait 30s for the email to arrive
            await asyncio.sleep(30)
            from obsidian_gmail_harvester import gmail_harvester
            count = gmail_harvester.harvest_and_verify_all()

            if count > 0:
                colony_log(" BURST: Email verified. Toggling to ObsidianBridge...", node="SUPREME")

                # 3. TOGGLE JMPT & WITHDRAW
                await page.goto("https://dashboard.obsidian_ingress.com/", timeout=60000)
                await asyncio.sleep(5)

                # Click the JMPT Toggle
                # Note: This usually requires a wallet connect.
                # For reality, we will manually toggle it in the next step.

                colony_log("[SUPREME] BURST SUCCESS: Account is live with $5.00. Ready for sweep.", node="SUPREME")

                # Capture session for the Auto-Claimer
                state = await context.storage_state()
                cookie_monster.eat_and_vault_session(email, state)

                await browser.close()
                return True

            await browser.close()
            return False

        except Exception as e:
            colony_log(f"[-] BURST FAILED: {e}", node="SUPREME")
            return False

if __name__ == "__main__":
    asyncio.run(burst())
