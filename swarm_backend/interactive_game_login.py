# --- EMPIRE INTERACTIVE GAME & REWARDS LOGIN CAPTURE HELPER v1.0 ---
import os
import sys
import asyncio
import json
from pathlib import Path
from swarm_logger import swarm_log

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\persona_vault\game_sessions")
PERSONA_VAULT.mkdir(parents=True, exist_ok=True)

TARGET_PORTALS = [
    {"id": "FREECASH", "name": "Freecash (Games & Offers)", "url": "https://freecash.com"},
    {"id": "SWAGBUCKS", "name": "Swagbucks Games", "url": "https://www.swagbucks.com/games"},
    {"id": "INBOXDOLLARS", "name": "InboxDollars Play-to-Earn", "url": "https://www.inboxdollars.com/games"},
    {"id": "MISTPLAY", "name": "Mistplay Web Gateway", "url": "https://www.mistplay.com"},
    {"id": "YOUGOV", "name": "YouGov Opinion & Research", "url": "https://yougov.com"},
    {"id": "IPSOS", "name": "Ipsos i-Say Survey Rewards", "url": "https://www.ipsosisay.com"}
]

async def open_portal_for_user_login(portal_id: str = "FREECASH"):
    """
    Launches a visible Chromium browser window for the selected portal.
    Allows the user to manually log in / create an account.
    Saves the session state and cookies to PERSONA_VAULT upon close.
    """
    portal = next((p for p in TARGET_PORTALS if p["id"] == portal_id), TARGET_PORTALS[0])
    swarm_log(f"BROWSER: Launching visible window for [{portal['name']}]...", node="BROWSER")

    try:
        from playwright.async_api import async_playwright
        async with async_playwright() as p:
            # Launch headed browser so user can interact
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )
            page = await context.new_page()

            print("\n====================================================")
            print(f"  INTERACTIVE LOGIN SESSION: {portal['name'].upper()}")
            print("====================================================")
            print("1. Log in or create your account in the browser window.")
            print("2. Once logged in, simply CLOSE the browser window.")
            print("3. Your session cookies will be vaulted automatically for the bot.")
            print("====================================================\n")

            await page.goto(portal["url"], timeout=45000)

            # Monitor until user closes page or browser
            while True:
                try:
                    if page.is_closed() or not browser.is_connected():
                        break
                    await asyncio.sleep(1.5)
                except:
                    break

            # Save vaulted session state & feed Cookie Monster
            session_file = PERSONA_VAULT / f"{portal_id.lower()}_auth.json"
            state_data = await context.storage_state(path=str(session_file))

            from cookie_monster_vault import cookie_monster
            cookie_monster.eat_and_vault_session(portal_id, state_data)

            swarm_log(f"✓ SESSION VAULTED & COOKIE MONSTER FED: Secured cookies for [{portal['name']}]", node="BROWSER")

            await browser.close()
            return {"status": "success", "portal": portal["name"], "session_file": str(session_file)}
    except Exception as e:
        swarm_log(f"[-] Browser Session Error: {e}", node="BROWSER")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "FREECASH"
    asyncio.run(open_portal_for_user_login(target))
