# --- WILLOW RAIN SECURITY: OBSIDIAN HEADED INSPECTOR v2.0 (DIRECT BURST) ---
import asyncio
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
SESSION_FILE = PERSONA_VAULT / "cookie_monster" / "cookie_monster_obsidian_bridge.json"

async def inspect_live_node():
    """
    Opens a VISIBLE (headed) browser window DIRECTLY to the dashboard.
    Bypasses local proxy issues to ensure the Director can see the real-world status.
    """
    print(f"[SUPREME] INSPECTOR v2.0: Opening visible dashboard (DIRECT)...")

    if not SESSION_FILE.exists():
        print("Error: No session keys found. Log in first.")
        return

    async with async_playwright() as p:
        # Launch visible browser
        browser = await p.chromium.launch(headless=False)

        # Create context with Director's cookies (NO PROXY for this visual audit)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
        )

        with open(SESSION_FILE, 'r') as f:
            state = json.load(f)
            await context.add_cookies(state.get("cookies", []))

        page = await context.new_page()

        print("\n[!] WINDOW OPENING: You are now looking at your REAL Obsidian Ingress dashboard.")
        print("[!] Verify the balance ($0.67) and the active device count.")

        await page.goto("https://dashboard.obsidian_ingress.com/", timeout=0)

        # Keep alive until Director closes it
        while browser.is_connected():
            await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(inspect_live_node())
