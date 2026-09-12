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

# Correct Path after the Saturn/Obsidian rebrand purge
JMPT_SESSION = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\persona_vault\cookie_monster\cookie_monster_jumptask.json")

async def read_truth():
    print("🔱 PAYOUT_TRUTH_SCRAPE: Searching for the Director's $0.05...")

    if not JMPT_SESSION.exists():
        print(f"Error: Session file {JMPT_SESSION} does not exist.")
        return

    async with async_playwright() as p:
        try:
            # Launch in visible mode briefly to ensure we get the right DOM state
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(JMPT_SESSION))
            page = await context.new_page()

            print("   -> Navigating to JumpTask Dashboard...")
            await page.goto("https://app.jumptask.io/dashboard", timeout=60000, wait_until="networkidle")
            await asyncio.sleep(15) # Wait for rewards to settle

            # Extract EVERY NUMBER with a $ sign or credit label
            data = await page.evaluate("""() => {
                const results = [];
                document.querySelectorAll('div, span, p, h1, h2').forEach(el => {
                    const text = el.innerText.trim();
                    if (text.includes('$') || /^[0-9,.]+$/.test(text)) {
                        results.push(text);
                    }
                });
                return results;
            }""")

            print("\n--- RAW DATA FOUND ON SCREEN ---")
            found_005 = False
            for d in set(data):
                if len(d) < 30:
                    print(f"  [SIGNAL] {d}")
                    if "0.05" in d:
                        found_005 = True

            if found_005:
                print("\n🎯 CONFIRMED: Found $0.05. Director is correct. System numbers were WRONG.")
            else:
                print("\n[!] ALERT: $0.05 NOT FOUND. The bot is seeing different data.")

            await browser.close()
        except Exception as e:
            print(f"[-] Scrape error: {e}")

if __name__ == "__main__":
    asyncio.run(read_truth())
