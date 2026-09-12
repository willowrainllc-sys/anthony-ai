import asyncio
from playwright.async_api import async_playwright
import sys
sys.path.append('colony_backend')
from playwright_stealth_factory import stealth_factory

async def search():
    async with async_playwright() as p:
        browser, context = await stealth_factory.create_stealth_context(p, headless=True)
        page = await context.new_page()
        print("Navigating to Rayobyte...")
        await page.goto('https://rayobyte.com/', timeout=60000)
        await asyncio.sleep(5)

        links = await page.eval_on_selector_all('a', 'elements => elements.map(el => ({text: el.innerText, href: el.href}))')
        for l in links:
            txt = l.get('text', '').lower()
            if any(k in txt for k in ['contact', 'partner', 'become', 'provider']):
                print(f"MATCH: {l['text']} -> {l['href']}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(search())
