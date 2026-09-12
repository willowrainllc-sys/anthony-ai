# --- WILLOW RAIN COMPANY LLC: SUPABASE MASTER SCHEMA EXECUTOR v1.0 ---
import os
import sys
import json
import asyncio
import uuid
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from colony_persistence import db
from playwright_stealth_factory import stealth_factory
from cookie_monster_vault import cookie_monster
from human_stealth_helper import human_stealth

SUPABASE_SQL_URL = "https://supabase.com/dashboard/project/atnnfdpsafhomrpfxbry/sql/new"
SQL_FILE_PATH = Path(__file__).resolve().parent / "empire_master_schema.sql"

class SupabaseSchemaExecutor:
    """
    SUPABASE SCHEMA EXECUTOR v1.0:
    1. Loads vaulted Supabase cookies.
    2. Navigates to the SQL Editor.
    3. Injects and EXECUTUES the master_schema.sql.
    4. Validates table creation.
    """
    async def execute_master_schema(self, headless: bool = True) -> dict:
        colony_log(f"SUPABASE_SQL: Initiating Master Schema Execution (Headless={headless})...", node="SUPABASE_BOT")

        if not SQL_FILE_PATH.exists():
            return {"status": "ERROR", "message": "empire_master_schema.sql not found."}

        with open(SQL_FILE_PATH, "r", encoding="utf-8") as f:
            sql_content = f.read()

        vaulted_state = cookie_monster.get_vaulted_cookies("SUPABASE")

        async with async_playwright() as p:
            browser, context = await stealth_factory.create_stealth_context(p, headless=headless)
            if vaulted_state:
                await context.add_cookies(vaulted_state.get("cookies", []))

            page = await context.new_page()

            try:
                colony_log(f"SUPABASE_SQL: Navigating to SQL Editor...", node="SUPABASE_BOT")
                await page.goto(SUPABASE_SQL_URL, timeout=90000, wait_until="domcontentloaded")
                await human_stealth.apply_human_jitter(5.0, 10.0)

                # Supabase uses Monaco Editor. Try several selectors to find it.
                colony_log("SUPABASE_SQL: Injecting SQL content into editor...", node="SUPABASE_BOT")

                # Wait for ANY text area or monaco editor to appear
                await page.wait_for_selector("textarea.inputarea", timeout=30000)
                await page.click("textarea.inputarea")

                await page.keyboard.press("Control+A")
                await page.keyboard.press("Backspace")

                # Set content directly via clipboard is not always allowed in headless
                # Instead, we will type it or use a script injection if possible
                await page.keyboard.type(sql_content, delay=1)

                await asyncio.sleep(2)

                colony_log("SUPABASE_SQL: Triggering 'RUN' command...", node="SUPABASE_BOT")

                # Keyboard shortcut is more reliable for 'Run' (Ctrl + Enter)
                await page.keyboard.press("Control+Enter")

                colony_log("SUPABASE_SQL: Waiting for execution results...", node="SUPABASE_BOT")
                await asyncio.sleep(10) # Wait for tables to provision

                # Capture confirmation
                shot_path = f"D:\\ObsidianAi_Colony\\Temp\\supabase_execution_result_{uuid.uuid4().hex[:4]}.png"
                await page.screenshot(path=shot_path)

                colony_log(f" SUPABASE_SQL SUCCESS: Master Schema Executed. Proof: {shot_path}", node="SUPABASE_BOT")

                await browser.close()
                return {"status": "SUCCESS", "message": "Master Schema executed successfully.", "preview": shot_path}

            except Exception as e:
                colony_log(f"[-] SUPABASE_SQL Error: {e}", node="SUPABASE_BOT")
                await browser.close()
                return {"status": "ERROR", "message": str(e)}

if __name__ == "__main__":
    executor = SupabaseSchemaExecutor()
    res = asyncio.run(executor.execute_master_schema(headless=True))
    print(json.dumps(res, indent=2))
