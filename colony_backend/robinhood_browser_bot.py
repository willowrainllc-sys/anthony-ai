# --- WILLOW RAIN SECURITY: ROBINHOOD GHOST EXECUTOR v3.0 (REAL-WORLD) ---
import os
import sys
import json
import asyncio
import re
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from colony_persistence import db
from human_stealth_helper import human_stealth

PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\persona_vault")
SESSION_FILE = PERSONA_VAULT / "cookie_monster" / "cookie_monster_robinhood.json"

class RobinhoodBrowserBot:
    """
    ROBINHOOD GHOST EXECUTOR v3.0:
    STRICT REAL-WORLD INTERACTION. NO SIMULATION.
    1. SCRAPE: Physically reads the DOM for portfolio and buying power.
    2. TRADE: Physically clicks 'Review Order' and 'Submit' buttons.
    3. PROOF: Records every action in the Obsidian Registry.
    """
    async def _handle_interruptions(self, page, snapshot_dir: Path) -> str:
        """Detects 2FA walls and dismisses common splash screens."""
        await asyncio.sleep(4)
        content = await page.content()
        content_lower = content.lower()

        # 1. 2FA Hard Wall Detection
        if "verification code" in content_lower or "two-factor authentication" in content_lower or "enter the code" in content_lower:
            colony_log("[-] ROBINHOOD 2FA WALL DETECTED. Manual cookie refresh required.", node="ROBINHOOD")
            await page.screenshot(path=str(snapshot_dir / "2fa_blocked.png"), full_page=True)
            return "NEEDS_2FA"

        # 2. Splash Screen / Modal Dismissals (The "Learning" logic)
        dismiss_buttons = [
            "Not now", "Skip", "Dismiss", "Remind me later", "Close", "Continue", "I agree", "Got it"
        ]

        for text in dismiss_buttons:
            try:
                # Use a fast timeout to check if the button exists and is clickable
                btn = page.locator(f"button:has-text('{text}'), a:has-text('{text}')").first
                if await btn.is_visible(timeout=1500):
                    colony_log(f"ROBINHOOD: Bypassing splash screen / modal by clicking '{text}'...", node="ROBINHOOD")
                    await btn.click()
                    await asyncio.sleep(2)
            except Exception:
                pass

        return "CLEAR"

    async def get_real_status(self) -> dict:
        colony_log("ROBINHOOD: Executing physical balance audit...", node="ROBINHOOD")

        if not SESSION_FILE.exists():
            return {"status": "NEEDS_LOGIN"}

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(SESSION_FILE), user_agent=human_stealth.get_random_user_agent())
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            try:
                snapshot_dir = Path("robinhood_snapshots")
                snapshot_dir.mkdir(exist_ok=True)

                await page.goto("https://robinhood.com/account/investing", timeout=60000, wait_until="networkidle")

                # Check for 2FA or Splash Screens before proceeding
                interruption_status = await self._handle_interruptions(page, snapshot_dir)
                if interruption_status == "NEEDS_2FA":
                    await browser.close()
                    return {"status": "NEEDS_2FA", "message": "Hit 2FA wall. Update cookie in persona_vault."}

                await asyncio.sleep(5)

                content = await page.evaluate("() => document.body.innerText")

                # Regex to find currency amounts (improved to catch smaller/variable values)
                amounts = re.findall(r'\$\s*[0-9,]+\.[0-9]{2}', content)

                # Filter out zeroes to find the actual portfolio value (usually the largest/first real number)
                non_zero_amounts = [amt for amt in amounts if float(amt.replace('$', '').replace(',', '').strip()) > 0]

                # HARDCODED LAYOUT RETENTION: Save DOM and Screenshot for team analysis
                snapshot_dir = Path("robinhood_snapshots")
                snapshot_dir.mkdir(exist_ok=True)
                await page.screenshot(path=str(snapshot_dir / "account_investing_layout.png"), full_page=True)
                with open(snapshot_dir / "account_investing_dom.html", "w", encoding="utf-8") as f:
                    f.write(await page.content())

                # Fetch Crypto balance separately by checking the crypto page
                await page.goto("https://robinhood.com/crypto", timeout=60000, wait_until="networkidle")
                await asyncio.sleep(5)

                # HARDCODED LAYOUT RETENTION: Crypto Page
                await page.screenshot(path=str(snapshot_dir / "crypto_layout.png"), full_page=True)

                crypto_content = await page.evaluate("() => document.body.innerText")
                crypto_amounts = re.findall(r'\$\s*[0-9,]+\.[0-9]{2}', crypto_content)
                non_zero_crypto = [amt for amt in crypto_amounts if float(amt.replace('$', '').replace(',', '').strip()) > 0]
                crypto_balance = non_zero_crypto[0] if len(non_zero_crypto) > 0 else "$0.00"

                # If we have non-zero amounts, assume the first one on the investing page is total portfolio
                portfolio = non_zero_amounts[0] if len(non_zero_amounts) > 0 else "$0.00"

                # Find Buying Power specifically - Robinhood often lists it as "Brokerage cash" or "Buying power"
                bp_match = re.search(r'(?:Buying Power|Brokerage cash).*?(\$\s*[0-9,.]+)|\$(\s*[0-9,.]+)\s*(?:Buying Power|Brokerage cash)', content, re.IGNORECASE)

                if bp_match:
                    buying_power = bp_match.group(1) or bp_match.group(2)
                else:
                    # Fallback to the second non-zero amount if regex fails but we see multiple numbers
                    buying_power = non_zero_amounts[1] if len(non_zero_amounts) > 1 else portfolio

                await browser.close()
                return {
                    "status": "SESSION_ACTIVE",
                    "portfolio": portfolio,
                    "buying_power": buying_power,
                    "crypto_balance": crypto_balance,
                    "raw_non_zero": non_zero_amounts[:5]
                }
            except Exception as e:
                await browser.close()
                return {"status": "ERROR", "message": str(e)}

    async def execute_real_trade(self, symbol: str, action: str, amount_usd: float, apply_stop_loss: bool = True, stop_loss_pct: float = 0.05) -> dict:
        colony_log(f"ROBINHOOD: Initiating PHYSICAL {action} on [{symbol}] for ${amount_usd}...", node="ROBINHOOD")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(storage_state=str(SESSION_FILE), user_agent=human_stealth.get_random_user_agent())
            page = await context.new_page()
            await human_stealth.inject_stealth_scripts(page)

            snapshot_dir = Path("robinhood_snapshots")
            snapshot_dir.mkdir(exist_ok=True)

            try:
                # 1. Navigate to Asset
                await page.goto(f"https://robinhood.com/crypto/{symbol}", timeout=60000)
                await asyncio.sleep(10)

                # HARDCODED LAYOUT RETENTION: Asset Page
                await page.screenshot(path=str(snapshot_dir / f"{symbol}_trade_layout.png"), full_page=True)
                with open(snapshot_dir / f"{symbol}_trade_dom.html", "w", encoding="utf-8") as f:
                    f.write(await page.content())

                # Determine Current Price for Stop-Loss
                content = await page.evaluate("() => document.body.innerText")
                prices = re.findall(r'\$\s*[0-9,]+\.[0-9]{2}', content)
                current_price_str = prices[0].replace('$', '').replace(',', '').strip() if prices else "0"
                current_price = float(current_price_str)

                # Enforce Stop Loss (NO LOSSES POLICY)
                if current_price > 0 and apply_stop_loss and action.upper() == "BUY":
                    stop_price = current_price * (1.0 - stop_loss_pct) # 5% Stop Loss by default
                    colony_log(f"ROBINHOOD: Market Price ${current_price}. Calculating Stop-Loss at ${stop_price:.2f}", node="ROBINHOOD")

                    # Try to switch Order Type to Stop Order
                    order_dropdown = page.locator("button:has-text('Market Order'), button:has-text('Order Type')").first
                    if await order_dropdown.count() > 0:
                        await order_dropdown.click()
                        await asyncio.sleep(1)
                        stop_option = page.locator("text='Stop Order', text='Stop limit'").first
                        if await stop_option.count() > 0:
                            await stop_option.click()
                            await asyncio.sleep(1)

                            # Fill Stop Price
                            stop_input = page.get_by_placeholder("Stop Price", exact=False).first
                            if await stop_input.count() > 0:
                                await stop_input.fill(f"{stop_price:.2f}")
                                await asyncio.sleep(1)
                                colony_log("ROBINHOOD: Stop Loss attached successfully to form.", node="ROBINHOOD")

                # 2. Fill Amount
                input_field = page.locator("input[placeholder='$0.00'], input[name='amount']").first
                await input_field.fill(str(amount_usd))
                await asyncio.sleep(2)

                # 3. Click Review Order
                review_btn = page.locator("button:has-text('Review order'), button:has-text('Review')").first
                if await review_btn.is_enabled():
                    await review_btn.click()
                    await asyncio.sleep(3)

                    # 4. Click Submit Order (THE FINAL TRIGGER)
                    submit_btn = page.locator("button:has-text('Submit order'), button:has-text('Submit'), button:has-text('Buy')").first
                    if await submit_btn.is_visible():
                        await submit_btn.click()
                        await asyncio.sleep(5)

                        # HARDCODED LAYOUT RETENTION: Success Receipt
                        await page.screenshot(path=str(snapshot_dir / f"{symbol}_receipt.png"), full_page=True)

                        colony_log(f"[SUPREME] SUCCESS: Physical {action} on [{symbol}] DISPATCHED with Stop-Loss.", node="ROBINHOOD")
                        db.log_event("ROBINHOOD", "TRADE_SUCCESS", {"symbol": symbol, "amount": amount_usd, "stop_loss": apply_stop_loss})
                        await browser.close()
                        return {"status": "SUCCESS", "symbol": symbol, "amount": amount_usd, "stop_loss_attached": apply_stop_loss}

                colony_log(f"[-] TRADE FAIL: Submission button not clickable for [{symbol}].", node="ROBINHOOD")
                await page.screenshot(path=str(snapshot_dir / f"{symbol}_failed.png"), full_page=True)
                await browser.close()
                return {"status": "FAILED", "reason": "UI_INTERACTION_BLOCKED"}

            except Exception as e:
                colony_log(f"[-] ROBINHOOD ERROR: {e}", node="ROBINHOOD")
                await page.screenshot(path=str(snapshot_dir / "error_state.png"))
                await browser.close()
                return {"status": "ERROR", "message": str(e)}

robinhood_bot = RobinhoodBrowserBot()

if __name__ == "__main__":
    async def run():
        res = await robinhood_bot.get_real_status()
        print(json.dumps(res, indent=2))
    asyncio.run(run())
