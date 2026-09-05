# --- ANTHONY AI: ADVANCED DEV-LINKER BROWSER v1.3 ---
import asyncio
from playwright.async_api import async_playwright
import os
import uuid
import sqlite3
from swarm_logger import swarm_log

DB_PATH = r"C:\AnthonyAi_Swarm\Empire_Vault.db"
PERSONA_VAULT = r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\persona_vault"

async def launch_auth_browser():
    """
    Launches an advanced browser that targets developer/security entry points.
    Enables manual override for 'Dev Allowed' features and captures session.
    """
    swarm_log("BROWSER: Initializing Advanced Dev-Linker...", node="BROWSER")

    async with async_playwright() as p:
        # Using headed mode so user can interact
        browser = await p.chromium.launch(headless=False)

        bot_id = f"DISCIPLE_{uuid.uuid4().hex[:6].upper()}"
        bot_folder = os.path.join(PERSONA_VAULT, bot_id)
        os.makedirs(bot_folder, exist_ok=True)

        auth_file = os.path.join(bot_folder, "auth_state.json")

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        swarm_log(f"BROWSER: Target ID [{bot_id}]. Opening Security/Dev Entry Point...", node="BROWSER")

        # We go to the Security page which contains the "Dev" and "Advanced" toggles
        await page.goto("https://myaccount.google.com/security")

        print("====================================================")
        print(f"  MISSION: DEV-LINKING & AUTH CAPTURE [{bot_id}]")
        print("====================================================")
        print("1. Log in. If prompted, use the 'Advanced' options.")
        print("2. Navigate to 'App Passwords' or 'YouTube Advanced' if needed.")
        print("3. Ensure all 'Bot-Friendly' security toggles are set.")
        print("4. ONCE READY: Simply CLOSE THE BROWSER WINDOW.")
        print("5. The session will be vaulted for headless use.")
        print("====================================================")

        # Monitor for close
        while True:
            try:
                if page.is_closed() or not browser.is_connected():
                    break

                # Check if we moved to a dev-ready state
                if "feature_eligibility" in page.url:
                    swarm_log("✓ REACHED: Dev Feature Eligibility.", node="BROWSER")

                await asyncio.sleep(2)
            except:
                break

        # Capture session
        await context.storage_state(path=auth_file)
        swarm_log(f"✓ VAULTED: Session secured for {bot_id}.", node="BROWSER")

        # Register
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("""
                INSERT INTO neural_disciples (id, name, aura, style, specialty, status, last_active)
                VALUES (?, ?, '9', 'Hacker/Dev', 'Advanced Strike', 'ACTIVE', ?)
            """, (bot_id, f"Disciple_{bot_id[-4:]}", 0))
            conn.commit()
            conn.close()
            swarm_log(f"GRID: {bot_id} is now an Advanced Dev-Node.", node="BROWSER")
        except Exception as e:
            swarm_log(f"[-] DB_FAIL: {e}", node="BROWSER")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_auth_browser())
