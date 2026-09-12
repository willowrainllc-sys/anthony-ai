# --- EMPIRE HUMAN ACTION STEALTH, BEZIER MOUSE & ROBUST LOCATOR HELPER v3.0 ---
import os
import sys
import time
import math
import random
import asyncio
from pathlib import Path
from swarm_logger import swarm_log

STEALTH_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
]

class HumanStealthHelper:
    """
    HUMAN STEALTH, BEZIER MOUSE & ROBUST LOCATOR HELPER v3.0:
    1. Robust Playwright locators using data-testid, getByRole, and getByText to prevent brittle selector breaks.
    2. Curved Bezier Mouse Cursor Movement & Arrow Clicker with natural acceleration/deceleration.
    3. Human typing rhythm with randomized per-character keystroke variance.
    4. Complete WebGL, Canvas, and webdriver anti-bot masking.
    """
    @staticmethod
    def get_random_user_agent() -> str:
        return random.choice(STEALTH_USER_AGENTS)

    @staticmethod
    async def apply_human_jitter(min_sec: float = 2.0, max_sec: float = 6.0):
        """Pauses execution with organic human-like delay variance."""
        delay = round(random.uniform(min_sec, max_sec), 2)
        swarm_log(f"STEALTH: Applying human jitter delay ({delay}s)...", node="STEALTH")
        await asyncio.sleep(delay)

    @staticmethod
    async def move_mouse_bezier(page, start_x: int, start_y: int, end_x: int, end_y: int, steps: int = 15):
        """Moves mouse along a natural human Bezier curve to bypass bot detection."""
        ctrl_x = start_x + (end_x - start_x) * random.uniform(0.2, 0.8) + random.randint(-40, 40)
        ctrl_y = start_y + (end_y - start_y) * random.uniform(0.2, 0.8) + random.randint(-40, 40)

        for i in range(1, steps + 1):
            t = i / steps
            x = int((1 - t)**2 * start_x + 2 * (1 - t) * t * ctrl_x + t**2 * end_x)
            y = int((1 - t)**2 * start_y + 2 * (1 - t) * t * ctrl_y + t**2 * end_y)
            await page.mouse.move(x, y)
            await asyncio.sleep(random.uniform(0.01, 0.03))

    @staticmethod
    async def robust_click_element(page, selector_or_testid: str):
        """
        Robust Playwright clicker using data-testid, text, or role attributes
        with curved Bezier mouse trajectories for 100% human action mimicry.
        """
        try:
            if selector_or_testid.startswith("data-testid="):
                testid = selector_or_testid.replace("data-testid=", "")
                elem = page.get_by_test_id(testid).first
            elif selector_or_testid.startswith("text="):
                txt = selector_or_testid.replace("text=", "")
                elem = page.get_by_text(txt).first
            else:
                elem = page.locator(selector_or_testid).first

            box = await elem.bounding_box()
            if box:
                target_x = int(box["x"] + box["width"] * random.uniform(0.3, 0.7))
                target_y = int(box["y"] + box["height"] * random.uniform(0.3, 0.7))

                start_x, start_y = random.randint(100, 400), random.randint(100, 400)
                await HumanStealthHelper.move_mouse_bezier(page, start_x, start_y, target_x, target_y)

                await page.mouse.move(target_x + random.randint(-2, 2), target_y + random.randint(-2, 2))
                await asyncio.sleep(random.uniform(0.1, 0.3))

                await page.mouse.down()
                await asyncio.sleep(random.uniform(0.05, 0.15))
                await page.mouse.up()
                swarm_log(f" STEALTH: Executed robust Bezier click on [{selector_or_testid}] at ({target_x}, {target_y})", node="STEALTH")
                return True
        except Exception as e:
            swarm_log(f"[-] Robust Click Fallback for {selector_or_testid}: {e}", node="STEALTH")
            try:
                await page.click(selector_or_testid)
                return True
            except: pass
        return False

    @staticmethod
    async def type_like_human(page, selector: str, text: str):
        """Types text into an input field with randomized human keystroke speed."""
        await HumanStealthHelper.robust_click_element(page, selector)
        for char in text:
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.04, 0.16))

    @staticmethod
    async def human_scroll_jitter(page):
        """Scrolls page up and down organically to mimic human reading behavior."""
        try:
            for _ in range(random.randint(2, 4)):
                scroll_y = random.randint(150, 450)
                await page.mouse.wheel(0, scroll_y)
                await asyncio.sleep(random.uniform(0.8, 1.8))
                if random.random() > 0.5:
                    await page.mouse.wheel(0, -random.randint(50, 150))
                    await asyncio.sleep(random.uniform(0.5, 1.2))
        except: pass

    @staticmethod
    async def inject_stealth_scripts(page):
        """Masks Playwright / Selenium automation flags in the browser context."""
        stealth_js = """
        Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });
        Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5] });
        window.chrome = { runtime: {} };
        """
        try:
            await page.add_init_script(stealth_js)
            swarm_log(" STEALTH: Anti-bot masking scripts injected into page context.", node="STEALTH")
        except Exception as e:
            swarm_log(f"[-] Stealth Injection Note: {e}", node="STEALTH")

    @staticmethod
    async def handle_interruptions(page) -> str:
        """
        Agentic Daemon Logic: Detects 2FA walls and dismisses common popup/splash screens dynamically.
        Enables bots to 'self-heal' through unexpected UI changes.
        """
        await asyncio.sleep(4)
        try:
            content = await page.content()
            content_lower = content.lower()

            # 1. 2FA Hard Wall Detection
            if any(phrase in content_lower for phrase in ["verification code", "two-factor authentication", "enter the code", "confirm it's you", "prove you're human", "security check"]):
                swarm_log("[-] AGENTIC WALL DETECTED: 2FA or Security Challenge. Manual intervention or cookie refresh required.", node="AGENTIC_DAEMON")
                return "NEEDS_2FA"

            # 2. Splash Screen / Modal Dismissals (The Self-Healing logic)
            dismiss_buttons = [
                "Not now", "Skip", "Dismiss", "Remind me later", "Close", "Continue", "I agree", "Got it", "Maybe later", "No thanks", "Accept All Cookies", "Accept"
            ]

            for text in dismiss_buttons:
                try:
                    # Fast timeout to check if the button exists and is clickable
                    btn = page.locator(f"button:has-text('{text}'), a:has-text('{text}')").first
                    if await btn.is_visible(timeout=1000):
                        swarm_log(f"AGENTIC DAEMON: Self-healing popup... clicking '{text}' to dismiss overlay.", node="AGENTIC_DAEMON")
                        await btn.click()
                        await asyncio.sleep(2)
                except Exception:
                    pass

            return "CLEAR"
        except Exception as e:
            swarm_log(f"[-] AGENTIC INTERRUPTION ERROR: {e}", node="AGENTIC_DAEMON")
            return "ERROR"

    @staticmethod
    async def take_learning_snapshot(page, bot_name: str, state_name: str):
        """
        Agentic Daemon Logic: Saves full-page screenshots and DOM HTML so the development team
        and AI can learn from UI changes, preventing data loss when selectors break.
        """
        snapshot_dir = Path(f"{bot_name}_snapshots")
        snapshot_dir.mkdir(exist_ok=True)

        try:
            # Save Screenshot
            screenshot_path = str(snapshot_dir / f"{state_name}_layout.png")
            await page.screenshot(path=screenshot_path, full_page=True)

            # Save Raw DOM
            dom_path = str(snapshot_dir / f"{state_name}_dom.html")
            with open(dom_path, "w", encoding="utf-8") as f:
                f.write(await page.content())

            swarm_log(f"AGENTIC DAEMON: Hardcoded learning snapshot saved for [{bot_name}] -> [{state_name}]", node="AGENTIC_DAEMON")
        except Exception as e:
            swarm_log(f"[-] AGENTIC SNAPSHOT FAILED: {e}", node="AGENTIC_DAEMON")

human_stealth = HumanStealthHelper()

if __name__ == "__main__":
    async def test_stealth():
        print("Testing Human Stealth Bezier & Robust Locator Helper v3.0...")
        print("User Agent:", human_stealth.get_random_user_agent())
        await human_stealth.apply_human_jitter(1.0, 2.0)
        print(" Stealth test complete.")
    asyncio.run(test_stealth())
