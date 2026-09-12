import asyncio
import os
import json
import re
from pathlib import Path
from playwright.async_api import async_playwright

# Setup paths
sys_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(sys_path)

from human_stealth_helper import human_stealth
from playwright_stealth_factory import stealth_factory

SESSION_FILE = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_obsidian_bridge.json")

async def run_audit():
    print("🔱 FINAL_TRUTH_AUDIT: Resolving balance discrepancy...")

    if not SESSION_FILE.exists():
        print("Error: No session keys.")
        return

    async with async_playwright() as p:
        try:
            # Low resource mode
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                storage_state=str(SESSION_FILE),
                user_agent=human_stealth.get_random_user_agent(),
                viewport={'width': 800, 'height': 600}
            )
            page = await context.new_page()

            # 1. Navigate to Obsidian Bridge
            print("   -> Navigating to app.obsidian_bridge.io...")
            await page.goto("https://app.obsidian_bridge.io/dashboard", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(10)

            # 2. Extract specific labels and values
            stats = await page.evaluate("""() => {
                const results = [];
                document.querySelectorAll('span, p, div').forEach(el => {
                    const text = el.innerText.trim();
                    if (text.includes('$') || text.includes('JMPT')) {
                        results.push(text);
                    }
                });
                return results;
            }""")

            print("\n--- ALL MONETARY VALUES ON SCREEN ---")
            for s in stats[:20]:
                if len(s) < 50:
                    print(f"  [SIGNAL] {s}")

            # 3. Check for specific "Obsidian Ingress" line item
            try:
                hg_val = await page.get_by_text("Obsidian Ingress", exact=False).first.inner_text()
                print(f"\n[✓] SPECIFIC OBSIDIAN_INGRESS STAT: {hg_val}")
            except: pass

            await browser.close()
        except Exception as e:
            print(f"[-] Audit error: {e}")

if __name__ == "__main__":
    asyncio.run(run_audit())
