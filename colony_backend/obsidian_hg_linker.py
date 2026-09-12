# --- WILLOW RAIN SECURITY: OBSIDIAN OBSIDIAN_INGRESS-OBSIDIAN_BRIDGE LINKER v3.0 ---
import asyncio
import os
import json
import random
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from colony_persistence import db
from human_stealth_helper import human_stealth
from playwright_stealth_factory import stealth_factory

# Configuration
OBSIDIAN_BRIDGE_ID = "c54d9d74-fd16-4bfd-9136-904fb62ff21f"
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
COOKIE_MONSTER = PERSONA_VAULT / "cookie_monster"
TEMP_DIR = Path(r"D:\ObsidianAi_Colony\Temp")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

class Obsidian IngressLinker:
    """
    OBSIDIAN_INGRESS LINKER v3.0:
    Automates the connection of Obsidian Ingress accounts to the Director's ObsidianBridge ID.
    1. VAULT SCAN: Identifies all active Obsidian Ingress sessions.
    2. GHOST NAVIGATION: Logins via Playwright and navigates to the JMPT modal.
    3. ID INJECTION: Pastes the c54d9d74... ID and verifies the handshake.
    """
    async def link_account(self, auth_file: Path):
        account_name = auth_file.stem.replace("cookie_monster_", "")
        colony_log(f"LINKER: Processing [{account_name}] for ObsidianBridge binding...", node="SUPREME")

        async with async_playwright() as p:
            try:
                # Use mobile emulation for higher authority
                device = p.devices['Pixel 7']
                browser, context = await stealth_factory.create_stealth_context(p, headless=True)

                # Load cookies
                with open(auth_file, 'r') as f:
                    state = json.load(f)
                    await context.add_cookies(state.get("cookies", []))

                page = await context.new_page()
                await human_stealth.inject_stealth_scripts(page)

                # 1. Access Dashboard
                colony_log(f"   -> Accessing Obsidian Ingress for [{account_name}]...", node="SUPREME")
                await page.goto("https://dashboard.obsidian_ingress.com/", timeout=60000, wait_until="networkidle")
                await asyncio.sleep(5)

                # 2. Check if already linked
                content = await page.content()
                if OBSIDIAN_BRIDGE_ID in content:
                    colony_log(f"   [] ALREADY LINKED: [{account_name}] is already bound to ID.", node="SUPREME")
                    await browser.close()
                    return True

                # 3. Trigger Modal
                toggle = page.locator(".wallet-toggle")
                if await toggle.count() > 0:
                    await toggle.click()
                    await asyncio.sleep(2)

                # 4. Fill ID and Submit
                input_field = page.locator("input[placeholder*='Account ID'], input[name*='obsidian_bridge_id']")
                if await input_field.count() == 0:
                    input_field = page.get_by_role("textbox").last

                await input_field.fill(OBSIDIAN_BRIDGE_ID)
                await human_stealth.apply_human_jitter(1, 2)

                submit_btn = page.get_by_text("Add the account", exact=True).first
                if await submit_btn.count() > 0:
                    await submit_btn.click()
                    await asyncio.sleep(5)

                    colony_log(f" LINKER SUCCESS: Account [{account_name}] is now feeding ObsidianBridge.", node="SUPREME")
                    db.log_event("SUPREME", "ACCOUNT_LINKED_TO_JMPT", {"account": account_name, "jmpt_id": OBSIDIAN_BRIDGE_ID})
                    await browser.close()
                    return True

                await browser.close()
                return False

            except Exception as e:
                colony_log(f"[-] LINKER ERROR: {e}", node="SUPREME")
                return False

    async def execute_mass_linking_burst(self, limit: int = 50):
        auth_files = list(COOKIE_MONSTER.glob("cookie_monster_*.json"))
        # Filter for Obsidian Ingress accounts
        hg_files = [f for f in auth_files if "obsidian_ingress" in f.name or "ghost" in f.name or "node" in f.name or "obsidian_bridge" in f.name]

        colony_log(f"LINKER: Initiating mass burst on {len(hg_files)} accounts...", node="SUPREME")

        linked_count = 0
        for i in range(0, min(len(hg_files), limit), 5):
            batch = hg_files[i:i+5]
            tasks = [self.link_account(f) for f in batch]
            results = await asyncio.gather(*tasks)
            linked_count += sum(1 for r in results if r)
            await asyncio.sleep(random.uniform(5, 10))

        return linked_count

linker = Obsidian IngressLinker()

if __name__ == "__main__":
    asyncio.run(linker.execute_mass_linking_burst())
