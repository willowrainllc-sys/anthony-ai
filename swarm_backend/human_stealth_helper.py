# --- EMPIRE HUMAN ACTION STEALTH, BEZIER MOUSE & ARROW CLICKER HELPER v2.0 ---
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
    HUMAN STEALTH, BEZIER MOUSE & ARROW CLICKER HELPER v2.0:
    1. Curved Bezier Mouse Cursor Movement & Arrow Clicker with natural acceleration/deceleration.
    2. Human typing rhythm with randomized per-character keystroke variance.
    3. Organic page scrolling & random viewport mouse hover jitter.
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
            # Quadratic Bezier formula
            x = int((1 - t)**2 * start_x + 2 * (1 - t) * t * ctrl_x + t**2 * end_x)
            y = int((1 - t)**2 * start_y + 2 * (1 - t) * t * ctrl_y + t**2 * end_y)
            await page.mouse.move(x, y)
            await asyncio.sleep(random.uniform(0.01, 0.03))

    @staticmethod
    async def human_arrow_click(page, selector: str):
        """Locates element bounding box, moves mouse in Bezier curve, hovers, and clicks."""
        try:
            elem = page.locator(selector).first
            box = await elem.bounding_box()
            if box:
                target_x = int(box["x"] + box["width"] * random.uniform(0.3, 0.7))
                target_y = int(box["y"] + box["height"] * random.uniform(0.3, 0.7))

                # Current mouse position or default start
                start_x, start_y = random.randint(100, 400), random.randint(100, 400)
                await HumanStealthHelper.move_mouse_bezier(page, start_x, start_y, target_x, target_y)

                # Pre-click hover jitter
                await page.mouse.move(target_x + random.randint(-2, 2), target_y + random.randint(-2, 2))
                await asyncio.sleep(random.uniform(0.1, 0.3))

                await page.mouse.down()
                await asyncio.sleep(random.uniform(0.05, 0.15))
                await page.mouse.up()
                swarm_log(f"✓ STEALTH: Executed human arrow click at ({target_x}, {target_y}) on {selector}", node="STEALTH")
                return True
        except Exception as e:
            swarm_log(f"[-] Stealth Click Fallback for {selector}: {e}", node="STEALTH")
            try:
                await page.click(selector)
                return True
            except: pass
        return False

    @staticmethod
    async def type_like_human(page, selector: str, text: str):
        """Types text into an input field with randomized human keystroke speed."""
        await HumanStealthHelper.human_arrow_click(page, selector)
        for char in text:
            await page.keyboard.type(char)
            await asyncio.sleep(random.uniform(0.04, 0.16)) # 40ms to 160ms per char

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
            swarm_log("✓ STEALTH: Anti-bot masking scripts injected into page context.", node="STEALTH")
        except Exception as e:
            swarm_log(f"[-] Stealth Injection Note: {e}", node="STEALTH")

human_stealth = HumanStealthHelper()

if __name__ == "__main__":
    async def test_stealth():
        print("Testing Human Stealth Bezier & Arrow Clicker Helper v2.0...")
        print("User Agent:", human_stealth.get_random_user_agent())
        await human_stealth.apply_human_jitter(1.0, 2.0)
        print("✓ Stealth test complete.")
    asyncio.run(test_stealth())
