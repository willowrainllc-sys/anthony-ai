# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES GSC & VERCEL DOMAIN LINKER v7.0 ---
import asyncio
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from human_stealth_helper import human_stealth

class AresVercelGscLinker:
    def __init__(self):
        self.root_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
        self.profile_dir = self.root_dir / "secure_assets" / "ares_browser_profile"
        self.gmail_cookie_file = self.root_dir / "secure_assets" / "persona_vault" / "cookie_monster" / "cookie_monster_gmail.json"
        self.bursts_dir = self.root_dir / "secure_assets" / "recon_vault" / "ares_bursts"
        self.profile_dir.mkdir(parents=True, exist_ok=True)
        self.bursts_dir.mkdir(parents=True, exist_ok=True)

    async def execute_linker(self):
        colony_log("ARES VERCEL GSC: Launching automated management portals...", node="SUPREME")

        async with async_playwright() as p:
            browser_context = await p.chromium.launch_persistent_context(
                user_data_dir=str(self.profile_dir),
                headless=False,
                viewport={'width': 1366, 'height': 768},
                args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
            )

            if self.gmail_cookie_file.exists():
                try:
                    data = json.loads(self.gmail_cookie_file.read_text(encoding="utf-8"))
                    cookies = data.get("cookies", data if isinstance(data, list) else [])
                    if cookies:
                        await browser_context.add_cookies(cookies)
                except Exception:
                    pass

            # Page 1: Google Search Console
            page1 = await browser_context.new_page()
            await human_stealth.inject_stealth_scripts(page1)
            await page1.goto("https://search.google.com/search-console", wait_until="domcontentloaded")

            # Page 2: Vercel Domains Settings
            page2 = await browser_context.new_page()
            await human_stealth.inject_stealth_scripts(page2)
            await page2.goto("https://vercel.com/willowrainllc-sys/anthony-ai/settings/domains", wait_until="domcontentloaded")

            colony_log("[+] ARES PORTALS ACTIVE: Both GSC and Vercel DNS settings open.", node="SUPREME")
            print("\n" + "="*70)
            print("  [+] ARES GSC & VERCEL PORTALS OPENED")
            print("  TAB 1: Google Search Console")
            print("  TAB 2: Vercel Domain Settings")
            print("="*70 + "\n")

            await asyncio.sleep(900)
            await browser_context.close()

if __name__ == "__main__":
    linker = AresVercelGscLinker()
    asyncio.run(linker.execute_linker())
