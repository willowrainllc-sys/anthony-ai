# --- ANTHONY AI: FACEBOOK BOT CREATOR & AUTH LINKER v1.0 ---
import asyncio
from playwright.async_api import async_playwright
import os
import uuid
import sqlite3
from swarm_logger import swarm_log

DB_PATH = r"C:\AnthonyAi_Swarm\Empire_Vault.db"
PERSONA_VAULT = r"C:\Users\willo/OneDrive/Desktop/Anthony_Ai\secure_assets\persona_vault"

async def launch_facebook_linker():
    """
    Launches a browser specifically for Facebook account creation/linking.
    Captures session state for the new AI bot in the collection.
    """
    swarm_log("BROWSER: Initializing Facebook Bot Linker...", node="BROWSER")

    async with async_playwright() as p:
        # Standard Chromium launch
        browser = await p.chromium.launch(headless=False)

        bot_id = f"DISCIPLE_{uuid.uuid4().hex[:6].upper()}"
        bot_folder = os.path.join(PERSONA_VAULT, bot_id)
        os.makedirs(bot_folder, exist_ok=True)

        auth_file = os.path.join(bot_folder, "auth_state.json")

        # Use a high-fidelity mobile user agent to look like a real device
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1"
        )
        page = await context.new_page()

        swarm_log(f"BROWSER: Target ID [{bot_id}]. Opening Facebook...", node="BROWSER")

        # Go to Facebook login/registration
        await page.goto("https://m.facebook.com/")

        print("====================================================")
        print(f"  MISSION: FACEBOOK BOT CREATION [{bot_id}]")
        print("====================================================")
        print("1. Log in or Create a new Facebook account.")
        print("2. Navigate to the Page you want this bot to manage.")
        print("3. IMPORTANT: Once you are ready, CLOSE THE BROWSER WINDOW.")
        print("4. I will lock the session state for the bot's headless strikes.")
        print("====================================================")

        # Monitor for close
        while True:
            try:
                if page.is_closed() or not browser.is_connected():
                    break
                await asyncio.sleep(2)
            except:
                break

        # Capturing the full state (Cookies, LocalStorage, etc.)
        await context.storage_state(path=auth_file)
        swarm_log(f"✓ VAULTED: Facebook session secured for {bot_id}.", node="BROWSER")

        # Register in DB
        try:
            conn = sqlite3.connect(DB_PATH)
            conn.execute("""
                INSERT INTO neural_disciples (id, name, aura, style, specialty, status, last_active)
                VALUES (?, ?, '6', 'Social-Stealth', 'Facebook Strike', 'ACTIVE', ?)
            """, (bot_id, f"FB_Bot_{bot_id[-4:]}", 0))
            conn.commit()
            conn.close()
            swarm_log(f"GRID: {bot_id} is now an active Facebook Disciple.", node="BROWSER")
        except Exception as e:
            swarm_log(f"[-] DB_FAIL: {e}", node="BROWSER")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_facebook_linker())
