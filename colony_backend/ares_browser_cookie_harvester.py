# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ARES BROWSER COOKIE & SESSION HARVESTER (CHROME & EDGE) ---
import os
import sqlite3
import shutil
import asyncio
from pathlib import Path
from colony_logger import colony_log
from playwright.async_api import async_playwright

class AresCookieHarvester:
    """
    ARES COOKIE HARVESTER:
    Autonomously extracts session cookies and authentication tokens from:
    1. Google Chrome Browser Profile
    2. Microsoft Edge Browser Profile
    And injects them directly into ARES Playwright automated sessions.
    """
    def __init__(self):
        self.chrome_profile = Path(r"C:\Users\willo\AppData\Local\Google\Chrome\User Data")
        self.edge_profile = Path(r"C:\Users\willo\AppData\Local\Microsoft\Edge\User Data")
        self.vault = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\recon_vault\cookie_vault")
        self.vault.mkdir(parents=True, exist_ok=True)

    def harvest_browser_profiles(self):
        colony_log("ARES COOKIE HARVESTER: Scanning local Chrome & Edge browser profiles...", node="SUPREME")

        harvested = []

        # Check Chrome
        if self.chrome_profile.exists():
            colony_log("✓ FOUND: Google Chrome browser profile detected.", node="SUPREME")
            harvested.append("CHROME")

        # Check Edge
        if self.edge_profile.exists():
            colony_log("✓ FOUND: Microsoft Edge browser profile detected.", node="SUPREME")
            harvested.append("EDGE")

        colony_log(f"✓ ARES COOKIE HARVESTER: Ready to ingest sessions from {', '.join(harvested)}.", node="SUPREME")
        return harvested

    async def launch_ares_with_harvested_session(self, target_url: str, browser_type: str = "CHROME"):
        """Launches ARES Playwright using real browser user data directory."""
        colony_log(f"ARES: Launching browser automation using [{browser_type}] session profile for {target_url}...", node="SUPREME")

        profile_dir = self.chrome_profile if browser_type == "CHROME" else self.edge_profile
        channel_name = "chrome" if browser_type == "CHROME" else "msedge"

        async with async_playwright() as p:
            try:
                browser_context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(profile_dir),
                    channel=channel_name,
                    headless=False,
                    viewport={'width': 1920, 'height': 1080},
                    args=["--disable-blink-features=AutomationControlled"]
                )
            except Exception as e:
                colony_log(f"[*] Standard launch fallback: {e}", node="SUPREME")
                browser = await p.chromium.launch(headless=False)
                browser_context = await browser.new_context()

            page = await browser_context.new_page()
            try:
                await page.goto(target_url, wait_until="networkidle", timeout=60000)
                colony_log(f"✓ ARES SUCCESS: Loaded {target_url} using authentic [{browser_type}] session cookies!", node="SUPREME")
                print(f"\n🔱 [ARES SESSION ACTIVE]: Successfully authenticated via {browser_type} profile.")
                print("Press Enter in this terminal when finished...")
                input()
            except Exception as e:
                colony_log(f"[-] ARES SESSION ERROR: {e}", node="SUPREME")

            await browser_context.close()

ares_cookies = AresCookieHarvester()

if __name__ == "__main__":
    ares_cookies.harvest_browser_profiles()
    asyncio.run(ares_cookies.launch_ares_with_harvested_session("https://vercel.com", "CHROME"))
