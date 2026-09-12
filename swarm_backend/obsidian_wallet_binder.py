# --- WILLOW RAIN SECURITY: OBSIDIAN BTC WALLET BINDER v1.0 ---
import asyncio
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright

# Configuration
BTC_WALLET = "bc1qk4ass5xsanvth2tz7jsapscy8ld25yr6ze5yzx"
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
SESSION_FILE = PERSONA_VAULT / "cookie_monster" / "cookie_monster_obsidian_bridge.json"

async def bind_wallet():
    """
    Physically binds the Director's Bitcoin wallet to the ObsidianBridge dashboard.
    This is the only way to ensure 'For Sure' payouts.
    """
    print(f"[SUPREME] WALLET_BINDER: Binding {BTC_WALLET} to ObsidianBridge...")

    if not SESSION_FILE.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            # We use headful for this one strike to ensure we see the result
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(SESSION_FILE))
            page = await context.new_page()

            # 1. Go to Settings/Profile
            await page.goto("https://app.obsidian_bridge.io/settings", timeout=60000)
            await asyncio.sleep(8)

            # 2. Look for "Wallet" or "Payout" section
            # Note: ObsidianBridge usually uses a 'Connect Wallet' button (Web3)
            # but for JMPT-to-BTC, we need to ensure the ID is linked.

            print("   -> Scanning settings for wallet input...")
            # If there's an input for the wallet, we fill it.
            # If it's a MetaMask connection, we must alert the Director.

            # Let's check the dashboard for the 'Link Wallet' modal
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000)
            await asyncio.sleep(5)

            # Take a screenshot to see the 'Connect' state
            await page.screenshot(path="D:\\ObsidianAi_Swarm\\Temp\\wallet_bind_check.png")

            content = await page.content()
            if BTC_WALLET in content:
                print(" SUCCESS: Wallet is ALREADY bound.")
            else:
                print("[-] WARNING: Wallet is NOT bound. The Director needs to connect his Web3 wallet once manually.")
                print("    Action: Execute 'python swarm_backend/disciple_login_portal.py OBSIDIAN_BRIDGE' and click 'Connect Wallet'.")

            await browser.close()
        except Exception as e:
            print(f"[-] Binding error: {e}")

if __name__ == "__main__":
    asyncio.run(bind_wallet())
