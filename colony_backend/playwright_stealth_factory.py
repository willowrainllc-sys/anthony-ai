# --- EMPIRE PLAYWRIGHT STEALTH FACTORY & NETWORK SPEED INTERCEPTOR v1.1 ---
import os
import sys
import json
import random
import asyncio
from pathlib import Path
from playwright.async_api import Playwright, Browser, BrowserContext, Page, Route
from colony_logger import colony_log
from human_stealth_helper import human_stealth

class NetworkInterceptor:
    BLOCKED_RESOURCE_TYPES = ["font", "media"]
    BLOCKED_DOMAINS = ["google-analytics.com", "doubleclick.net", "facebook.net"]

    @classmethod
    async def enable_fast_mode(cls, page: Page, block_images: bool = False):
        async def handle_route(route: Route):
            req = route.request
            if any(domain in req.url for domain in cls.BLOCKED_DOMAINS):
                await route.abort()
                return
            if req.resource_type in cls.BLOCKED_RESOURCE_TYPES or (block_images and req.resource_type == "image"):
                await route.abort()
                return
            await route.continue_()
        await page.route("**/*", handle_route)

class PlaywrightStealthFactory:
    @staticmethod
    async def create_stealth_context(
        p: Playwright,
        headless: bool = True,
        theme: str = "dark",
        fast_mode: bool = False,
        proxy: dict = None
    ) -> tuple[Browser, BrowserContext]:
        colony_log(f"STEALTH_FACTORY: Launching Chromium (Headless={headless}, Theme={theme}, Proxy={'Enabled' if proxy else 'None'})...", node="STEALTH_FACTORY")

        browser: Browser = await p.chromium.launch(
            headless=headless,
            channel="chrome",
            proxy=proxy,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )

        context: BrowserContext = await browser.new_context(
            user_agent=human_stealth.get_random_user_agent(),
            viewport={"width": 1280, "height": 800},
            color_scheme=theme,
            locale="en-US"
        )

        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        context.set_default_timeout(30000)
        return browser, context

stealth_factory = PlaywrightStealthFactory()
