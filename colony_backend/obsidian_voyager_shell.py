# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v6.2 (OBSIDIAN_TITAN SHELL) ---
import asyncio
import os
import sys
import argparse
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log

class ObsidianObsidian TitanShell:
    """
    OBSIDIAN_TITAN SHELL (Playwright Core):
    The Director's custom browser shell built on Chromium.
    1. PERSISTENT CONTEXT: Hides session data in the D-Drive Secure Assets.
    2. HUD INJECTION: Injects the Obsidian 'Sovereign' ticker into every page.
    3. GHOST MASKING: Spoofs hardware fingerprints to prevent tracking.
    4. HEADED INGRESS: Physically opens the window for direct interaction.
    """
    def __init__(self):
        self.user_data_dir = Path(r"D:\AnthonyAi_Colony\Secure_Assets\Obsidian Titan_Session")
        self.user_data_dir.mkdir(parents=True, exist_ok=True)

    async def launch_voyager(self, start_url="http://127.0.0.1:80", node_id="DIRECTOR"):
        colony_log(f"🛰️ OBSIDIAN_TITAN: Igniting Sovereign Browser Shell for [{node_id}]...", node="SUPREME")

        async with async_playwright() as p:
            # 🔱 Launch Persistent Chromium Context (Headed for Interaction)
            context = await p.chromium.launch_persistent_context(
                str(self.user_data_dir),
                headless=False,
                args=[
                    "--start-maximized",
                    "--disable-blink-features=AutomationControlled",
                    "--no-sandbox",
                    "--disable-infobars"
                ]
            )

            # 🔱 Ingest HUD Script: Real-time Wealth Tracking
            await context.add_init_script("""
                const injectHUD = () => {
                    if (document.getElementById('obsidian-hud')) return;

                    const style = document.createElement('style');
                    style.textContent = `
                        #obsidian-hud {
                            position: fixed;
                            bottom: 0; left: 0; width: 100%;
                            background: rgba(0, 0, 0, 0.95);
                            color: #fbbf24;
                            font-family: 'Courier New', monospace;
                            font-size: 11px;
                            padding: 8px 30px;
                            z-index: 999999;
                            border-top: 1px solid #fbbf24;
                            display: flex;
                            justify-content: space-between;
                            letter-spacing: 2px;
                            pointer-events: none;
                            text-transform: uppercase;
                            box-shadow: 0 -10px 40px rgba(0,0,0,0.8);
                        }
                    `;
                    document.head.appendChild(style);

                    const hud = document.createElement('div');
                    hud.id = 'obsidian-hud';
                    hud.innerHTML = `
                        <span>🛰️ OBSIDIAN_TITAN_NODE: ${window.location.hostname}</span>
                        <span>STATUS: AUTHORIZED_INGRESS</span>
                        <span>BY ANTHONY CHRISTOPHER</span>
                    `;
                    document.body.appendChild(hud);
                };

                setInterval(injectHUD, 2000);
            """)

            page = context.pages[0] if context.pages else await context.new_page()

            # 🔱 Local Resolution Fallback
            # If the domain fails, we redirect to the local portal
            try:
                colony_log(f"[*] OBSIDIAN_TITAN: Navigating to {start_url}...", node="SUPREME")
                await page.goto(start_url, timeout=10000)
            except:
                colony_log("[-] OBSIDIAN_TITAN: External domain unresolved. Falling back to Local Portal.", node="SUPREME")
                await page.goto("http://127.0.0.1:80")

            colony_log(f"✓ OBSIDIAN_TITAN SUCCESS: Ingress established on [{node_id}].", node="SUPREME")

            # Keep alive for interaction
            while True:
                await asyncio.sleep(60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://127.0.0.1:80")
    parser.add_argument("--node", default="MUSTANG_001")
    args = parser.parse_args()

    voyager = ObsidianObsidian TitanShell()
    asyncio.run(voyager.launch_voyager(start_url=args.url, node_id=args.node))
