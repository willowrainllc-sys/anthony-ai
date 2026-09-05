import asyncio
from playwright.async_api import async_playwright
import os

async def open_google_login():
    email = "j84611056@gmail.com"
    print(f"[*] Opening Google Login for {email} on PC...")

    async with async_playwright() as p:
        # Launching with a window (headed)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # 1. Start with Login
        await page.goto(f"https://accounts.google.com/ServiceLogin?Email={email}")

        print("====================================================")
        print(f"  ACTION REQUIRED: LOG IN AS {email}")
        print("====================================================")
        print("1. Complete the login manually in the browser window.")
        print("2. Once logged in, this script will auto-jump to Advanced Features.")
        print("====================================================")

        # 2. Wait for login to complete (look for account page)
        while True:
            if "myaccount.google.com" in page.url or "youtube.com" in page.url:
                print("[✓] Login detected. Redirecting to YouTube Advanced Features...")
                # Jump to Advanced Features
                await page.goto("https://studio.youtube.com/channel/UC/editing/settings/feature_eligibility")
                break
            await asyncio.sleep(2)
            if page.is_closed():
                return

        # Keep the browser open for the user to work
        try:
            while not page.is_closed():
                await asyncio.sleep(10)
        except KeyboardInterrupt:
            print("[*] Closing browser...")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(open_google_login())
