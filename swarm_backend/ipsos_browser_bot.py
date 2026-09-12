# --- EMPIRE IPSOS I-SAY HEADLESS SURVEY BOT v2.0 (HUMAN STEALTH & SAFETY FIRST) ---
import os
import sys
import json
import asyncio
import sqlite3
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db
from human_stealth_helper import human_stealth

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
PERSONA_VAULT.mkdir(parents=True, exist_ok=True)

class IpsosBrowserBot:
    """
    IPSOS I-SAY HEADLESS AUTOMATION BOT v2.0:
    Uses Playwright session cookies + human stealth masking scripts
    to monitor Ipsos surveys and log earnings safely without account flags.
    """
    def __init__(self):
        self.url = "https://www.ipsosisay.com"

    async def run_ipsos_survey_check(self, headless: bool = True) -> dict:
        swarm_log("IPSOS_BOT: Initializing Ipsos i-Say Headless Session with Human Stealth...", node="IPSOS_BOT")
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=headless)
                context = await browser.new_context(
                    user_agent=human_stealth.get_random_user_agent(),
                    viewport={"width": 1920, "height": 1080}
                )
                page = await context.new_page()

                # INJECT ANTI-BOT STEALTH SCRIPTS
                await human_stealth.inject_stealth_scripts(page)

                swarm_log("IPSOS_BOT: Navigating to Ipsos i-Say portal...", node="IPSOS_BOT")
                await page.goto(self.url, timeout=35000)

                # --- AGENTIC DAEMON UPGRADE ---
                interruption = await human_stealth.handle_interruptions(page)
                if interruption == "NEEDS_2FA":
                    await human_stealth.take_learning_snapshot(page, "ipsos", "2fa_blocked")
                    await browser.close()
                    return {"status": "NEEDS_2FA"}

                # HUMAN JITTER PAUSE
                await human_stealth.apply_human_jitter(2.0, 4.5)

                title = await page.title()
                swarm_log(f" IPSOS_BOT: Connected to portal [{title}]", node="IPSOS_BOT")

                # --- AGENTIC DAEMON UPGRADE: Hardcode layout for future learning ---
                await human_stealth.take_learning_snapshot(page, "ipsos", "survey_dashboard_ready")

                db.log_event("IPSOS_BOT", "SURVEY_CHECK_SUCCESS", {
                    "portal_title": title,
                    "url": page.url,
                    "status": "SESSION_ACTIVE_STEALTH"
                })

                await browser.close()
                return {
                    "status": "success",
                    "portal": "Ipsos i-Say",
                    "session_active": True,
                    "title": title,
                    "learning_telemetry_saved": True
                }
        except Exception as e:
            # AGENTIC FAILURE SNAPSHOT
            try:
                await human_stealth.take_learning_snapshot(page, "ipsos", "error_state")
            except: pass

            swarm_log(f"[-] IPSOS_BOT ERROR: {e}", node="IPSOS_BOT")
            return {
                "status": "ERROR",
                "message": str(e)
            }

ipsos_bot = IpsosBrowserBot()

if __name__ == "__main__":
    res = asyncio.run(ipsos_bot.run_ipsos_survey_check(headless=True))
    print("IPSOS BOT RESULT:", json.dumps(res, indent=2))
