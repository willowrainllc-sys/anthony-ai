# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v1.0 (UI CLONE BURST) ---
import asyncio
import os
import json
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log

RECON_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\recon_vault\obsidian city_ui_dna")
RECON_DIR.mkdir(parents=True, exist_ok=True)

class Obsidian CityUICloner:
    """
    OBSIDIAN CITY UI CLONER:
    Deep extraction of Obsidian City's consumer-friendly UX DNA.
    1. ELEMENT MAP: Captures every button, input, and section layout.
    2. STYLE ANALYZER: Extracts computed styles (colors, fonts, radii).
    3. TEXT PURGE: Scrapes their consumer-centric copy for rebranding.
    4. 3D VISUAL SYNC: Captures their usage of "3D" and "Hyper" imagery.
    """
    def __init__(self):
        self.target_url = "https://www.obsidian city.com"

    async def execute_cloning_burst(self):
        colony_log("CLONER: Initiating deep UI DNA capture on Obsidian City...", node="COMMAND")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = await context.new_page()

            try:
                await page.goto(self.target_url, wait_until="networkidle")

                # 🔱 1. Capture Full Page Map
                colony_log("[*] CLONER: Mapping page structure...", node="COMMAND")
                await page.screenshot(path=RECON_DIR / "obsidian city_full_structure.png", full_page=True)

                # 🔱 2. Extract Button DNA
                button_dna = await page.evaluate("""() => {
                    const buttons = Array.from(document.querySelectorAll('button, .btn, a.btn'));
                    return buttons.map(b => {
                        const style = window.getComputedStyle(b);
                        return {
                            text: b.innerText,
                            bg: style.backgroundColor,
                            color: style.color,
                            padding: style.padding,
                            radius: style.borderRadius,
                            font: style.fontFamily
                        };
                    });
                }""")

                # 🔱 3. Extract Core Headlines & Sections
                sections = await page.evaluate("""() => {
                    return Array.from(document.querySelectorAll('h1, h2, section')).map(s => ({
                        tag: s.tagName,
                        text: s.innerText.substring(0, 100),
                        classes: s.className
                    }));
                }""")

                # 🔱 4. Vault the DNA
                with open(RECON_DIR / "ui_dna_manifest.json", "w") as f:
                    json.dump({"buttons": button_dna, "sections": sections}, f, indent=4)

                colony_log("✓ CLONER SUCCESS: Obsidian City UI DNA vaulted.", node="COMMAND")

            except Exception as e:
                colony_log(f"[-] CLONER FAIL: {e}", node="COMMAND")

            await browser.close()

if __name__ == "__main__":
    cloner = Obsidian CityUICloner()
    asyncio.run(cloner.execute_cloning_burst())
