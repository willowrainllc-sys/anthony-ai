# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v1.0 (LIVE STUDIO VIEW) ---
import asyncio
import os
import sys
import time
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log

# Target File: Default to the new Marketplace
TARGET_FILE = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\willow_rain_global\wholesale_portal\obsidian_city_marketplace.html")
FILE_URL = f"file:///{str(TARGET_FILE).replace('\\', '/')}"

class ObsidianLiveStudio:
    """
    LIVE STUDIO VIEW:
    Headed Playwright session with Auto-Reload for the Director.
    1. VISUAL INGRESS: Opens the industrial HTML in a physical, headed browser.
    2. HOT RELOAD: Watches the file for changes and reloads the view instantly.
    3. LIVE AUDIT: Allows the Director to see UI edits happen in real-time.
    """
    def __init__(self):
        self.last_mtime = 0
        if TARGET_FILE.exists():
            self.last_mtime = os.path.getmtime(TARGET_FILE)

    async def run_live_session(self):
        colony_log(f"STUDIO: Launching Live View for [{TARGET_FILE.name}]...", node="SUPREME")

        async with async_playwright() as p:
            # 🔱 Launching HEADED mode - Director can see everything
            browser = await p.chromium.launch(headless=False, slow_mo=500)
            context = await browser.new_context(viewport={'width': 1440, 'height': 900})
            page = await context.new_page()

            colony_log("[*] STUDIO: Initial Ingress complete. Waiting for edits...", node="SUPREME")
            await page.goto(FILE_URL)

            try:
                while True:
                    # 🔱 Check for file updates
                    if TARGET_FILE.exists():
                        current_mtime = os.path.getmtime(TARGET_FILE)
                        if current_mtime > self.last_mtime:
                            colony_log(f"⚡ STUDIO: Change detected in {TARGET_FILE.name}. Reloading...", node="SUPREME")
                            await page.reload()
                            self.last_mtime = current_mtime

                    await asyncio.sleep(1) # Watch pulse

                    # Check if browser is still open
                    if page.is_closed():
                        break
            except Exception as e:
                colony_log(f"[-] STUDIO ERROR: {e}", node="SUPREME")

            colony_log("✓ STUDIO: Live View closed by Director.", node="SUPREME")
            await browser.close()

if __name__ == "__main__":
    studio = ObsidianLiveStudio()
    asyncio.run(studio.run_live_session())
