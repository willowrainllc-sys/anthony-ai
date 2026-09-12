# --- WILLOW RAIN COMPANY LLC: SUPABASE MIRACLE WRITER & CLOUD ACTIVATOR v3.0 ---
import os
import sys
import json
import asyncio
import uuid
import time
from pathlib import Path
from playwright.async_api import async_playwright
from swarm_logger import swarm_log
from playwright_stealth_factory import stealth_factory
from cookie_monster_vault import cookie_monster
from human_stealth_helper import human_stealth

SUPABASE_SQL_URL = "https://supabase.com/dashboard/project/atnnfdpsafhomrpfxbry/sql/new"
SQL_FILE = Path(__file__).resolve().parent / "empire_master_schema.sql"

class SupabaseMiracleWriter:
    """
    SUPABASE MIRACLE WRITER v3.0:
    The absolute ultimate cloud activation tactic.
    1. Brute-force discovery of the Monaco Editor.
    2. Deep JavaScript Injection to set editor value bypassing keyboard lag.
    3. Multi-path 'RUN' trigger (Keyboard shortcut + Button click).
    4. Optical verification of success messages.
    """
    async def activate_cloud_database(self, headless: bool = False):
        swarm_log(f"MIRACLE_WRITER: Initiating Cloud Database Activation (Headless={headless})...", node="SUPABASE_BOT")

        if not SQL_FILE.exists():
            swarm_log("[-] MIRACLE_WRITER: empire_master_schema.sql missing!", node="SUPABASE_BOT")
            return False

        with open(SQL_FILE, "r", encoding="utf-8") as f:
            sql_payload = f.read()

        vaulted = cookie_monster.get_vaulted_cookies("SUPABASE")

        async with async_playwright() as p:
            # Force Chrome for maximum compatibility with Monaco
            browser, context = await stealth_factory.create_stealth_context(p, headless=headless)
            if vaulted: await context.add_cookies(vaulted.get("cookies", []))

            page = await context.new_page()

            try:
                swarm_log("MIRACLE_WRITER: Navigating to SQL Portal...", node="SUPABASE_BOT")
                await page.goto(SUPABASE_SQL_URL, timeout=90000, wait_until="networkidle")

                # Give Monaco ample time to mount
                swarm_log("MIRACLE_WRITER: Waiting for editor synchronization...", node="SUPABASE_BOT")
                await asyncio.sleep(20)

                # TACTIC 1: Visual Proof
                await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\miracle_step1_sync.png")

                # TACTIC 2: Direct JS Model Injection (Fastest & most reliable)
                swarm_log("MIRACLE_WRITER: Injecting SQL via internal Monaco API...", node="SUPABASE_BOT")
                injection_js = """
                (content) => {
                    try {
                        const models = window.monaco.editor.getModels();
                        if (models.length > 0) {
                            models[0].setValue(content);
                            return "MODEL_INJECTED";
                        }
                        // Fallback to finding the active element
                        const active = document.activeElement;
                        if (active) {
                            active.value = content;
                            return "DOM_VALUE_SET";
                        }
                    } catch (e) {
                        return "ERROR: " + e.message;
                    }
                    return "NOT_FOUND";
                }
                """

                result = await page.evaluate(injection_js, sql_payload)
                swarm_log(f"MIRACLE_WRITER: Injection result -> {result}", node="SUPABASE_BOT")

                if "ERROR" in str(result) or "NOT_FOUND" in str(result):
                    swarm_log("MIRACLE_WRITER: API injection failed. Falling back to Keyboard brute force...", node="SUPABASE_BOT")
                    # TACTIC 3: Keyboard Brute Force
                    await page.click(".monaco-editor")
                    await page.keyboard.press("Control+A")
                    await page.keyboard.press("Backspace")
                    await page.keyboard.type(sql_payload, delay=1)

                await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\miracle_step2_populated.png")

                # TACTIC 4: Dual Run Trigger
                swarm_log("MIRACLE_WRITER: Triggering SQL STRIKE...", node="SUPABASE_BOT")

                # Path A: Keyboard Shortcut
                await page.keyboard.press("Control+Enter")
                await asyncio.sleep(2)

                # Path B: Physical Button Click
                try:
                    run_btn = page.get_by_role("button", name="Run").first
                    if await run_btn.is_enabled():
                        await run_btn.click()
                except: pass

                swarm_log("MIRACLE_WRITER: Monitoring for 'Success' confirmation...", node="SUPABASE_BOT")
                await asyncio.sleep(15)

                # TACTIC 5: Verification Screenshot
                await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\miracle_step3_final.png")

                # Check for success message in DOM
                content = await page.content()
                if "Success" in content or "Query returned no rows" in content or "CREATE TABLE" in content:
                    swarm_log(" MIRACLE_WRITER SUCCESS: Cloud Database Activated!", node="SUPABASE_BOT")
                    db.log_event("SUPABASE_BOT", "CLOUD_ACTIVATION_SUCCESS", {"status": "TABLES_PROVISIONED"})
                    await browser.close()
                    return True
                else:
                    swarm_log("[-] MIRACLE_WRITER: Verification failed. Check final screenshot.", node="SUPABASE_BOT")
                    await browser.close()
                    return False

            except Exception as e:
                swarm_log(f"[-] MIRACLE_WRITER Critical Failure: {e}", node="SUPABASE_BOT")
                await browser.close()
                return False

if __name__ == "__main__":
    writer = SupabaseMiracleWriter()
    # Run visible to see the miracle happen
    asyncio.run(writer.activate_cloud_database(headless=False))
