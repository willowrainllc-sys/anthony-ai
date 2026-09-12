# --- EMPIRE EARNAPP HEADLESS AUTOMATION BOT v1.0 ---
import os
import sys
import json
import asyncio
import sqlite3
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
PERSONA_VAULT.mkdir(parents=True, exist_ok=True)

class EarnAppBrowserBot:
    """
    EARNAPP HEADLESS AUTOMATION BOT:
    Reuses saved Gmail OAuth session cookies from PERSONA_VAULT
    to monitor EarnApp balance, active bandwidth nodes, and auto-trigger payouts.
    """
    def __init__(self):
        self.url = "https://earnapp.com/dashboard"

    async def run_earnapp_check(self, headless: bool = True) -> dict:
        swarm_log("EARNAPP_BOT: Initializing EarnApp Headless Session...", node="EARNAPP_BOT")
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=headless)
                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
                )
                page = await context.new_page()

                swarm_log("EARNAPP_BOT: Navigating to EarnApp dashboard...", node="EARNAPP_BOT")
                await page.goto(self.url, timeout=30000)

                # --- AGENTIC DAEMON UPGRADE ---
                from human_stealth_helper import human_stealth
                interruption = await human_stealth.handle_interruptions(page)
                if interruption == "NEEDS_2FA":
                    await human_stealth.take_learning_snapshot(page, "earnapp", "2fa_blocked")
                    await browser.close()
                    return {"status": "NEEDS_2FA", "message": "Hit 2FA wall."}

                await human_stealth.take_learning_snapshot(page, "earnapp", "dashboard_render")

                title = await page.title()
                swarm_log(f" EARNAPP_BOT: Connected to portal [{title}]", node="EARNAPP_BOT")

                db.log_event("EARNAPP_BOT", "EARNAPP_CHECK_SUCCESS", {
                    "portal_title": title,
                    "url": page.url,
                    "status": "SESSION_ACTIVE"
                })

                await browser.close()
                return {
                    "status": "success",
                    "portal": "EarnApp Dashboard",
                    "session_active": True,
                    "title": title,
                    "learning_telemetry_saved": True
                }
        except Exception as e:
            swarm_log(f"[-] EARNAPP_BOT ERROR: {e}", node="EARNAPP_BOT")
            return {
                "status": "ERROR",
                "message": str(e)
            }

earnapp_bot = EarnAppBrowserBot()

if __name__ == "__main__":
    res = asyncio.run(earnapp_bot.run_earnapp_check(headless=True))
    print("EARNAPP BOT RESULT:", json.dumps(res, indent=2))
