# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v1.0 (DNA EXTRACTOR) ---
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

RECON_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\recon_vault\godaddy_ui_dna")
RECON_DIR.mkdir(parents=True, exist_ok=True)

class DNAExtractor:
    def __init__(self):
        self.target = "https://www.godaddy.com/en-uk/websites/ai-website-builder"

    async def run_extraction(self):
        async with async_playwright() as p:
            # 🔱 High-trust user agent to bypass initial blocks
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(user_agent=user_agent)
            page = await context.new_page()

            swarm_log(f"EXTRACTOR: Hitting {self.target}...", node="RECON")
            await page.goto(self.target, wait_until="networkidle", timeout=60000)
            await asyncio.sleep(5) # Allow dynamic elements to settle


            # 🔱 1. Extract CSS Variables (Design Tokens)
            css_vars = await page.evaluate("""() => {
                const root = document.documentElement;
                const styles = window.getComputedStyle(root);
                const res = {};
                for (let i = 0; i < styles.length; i++) {
                    const prop = styles[i];
                    if (prop.startsWith("--")) res[prop] = styles.getPropertyValue(prop);
                }
                return res;
            }""")

            # 🔱 2. Extract Button DNA (Structure & Styles)
            button_dna = await page.evaluate("""() => {
                return Array.from(document.querySelectorAll('button, a[role="button"]')).slice(0, 10).map(b => {
                    const style = window.getComputedStyle(b);
                    return {
                        tag: b.tagName,
                        text: b.innerText.trim(),
                        bg: style.backgroundColor,
                        padding: style.padding,
                        radius: style.borderRadius,
                        font: style.fontFamily,
                        border: style.border
                    };
                });
            }""")

            # 🔱 3. Extract Layout Logic (Section Grids)
            layout_dna = await page.evaluate("""() => {
                return Array.from(document.querySelectorAll('section')).slice(0, 5).map(s => {
                    const style = window.getComputedStyle(s);
                    return {
                        id: s.id,
                        display: style.display,
                        gridTemplate: style.gridTemplateColumns,
                        padding: style.padding,
                        margin: style.margin
                    };
                });
            }""")

            # 🔱 4. Vault the DNA
            vault_file = RECON_DIR / "godaddy_raw_dna.json"
            with open(vault_file, 'w') as f:
                json.dump({
                    "design_tokens": css_vars,
                    "buttons": button_dna,
                    "layouts": layout_dna
                }, f, indent=4)

            print(f"✓ DNA EXTRACTION SUCCESS: {vault_file.name}")
            await browser.close()

if __name__ == "__main__":
    extractor = DNAExtractor()
    asyncio.run(extractor.run_extraction())
