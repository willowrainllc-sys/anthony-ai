# --- EMPIRE TEAM INTERACTION DEMO: VISUAL STRIKE v1.0 ---
import asyncio
import os
import random
import httpx
import json
from pathlib import Path
from playwright.async_api import async_playwright
from swarm_logger import swarm_log
from swarm_persistence import db

SECURE_DIR = Path(r"C:\AnthonyAi_Swarm\Secure")
TARGET_PAGE = "https://www.facebook.com/willowraincompanyllc"

async def generate_supportive_comment(post_text, bot_id):
    """Generates a high-fidelity comment using the Disciple's persona."""
    persona = {"name": "Alpha Node", "style": "Elite", "specialty": "Grid Intelligence"}
    try:
        with db._get_connection() as conn:
            row = conn.execute("SELECT name, style, specialty FROM neural_disciples WHERE id=?", (bot_id,)).fetchone()
            if row: persona = {"name": row[0], "style": row[1], "specialty": row[2]}
    except: pass

    prompt = f"""
    You are {persona['name']}, a {persona['style']} specialist in {persona['specialty']} for Willow Rain.
    You are viewing a new post on the main Willow Rain page: "{post_text[:150]}"

    MISSION:
    - Post a supportive, intelligent comment.
    - Advance the 'Alpha' narrative.
    - Sound like a loyal team member.
    - Under 20 words. NO BOT SLANG.

    Output: Raw comment text.
    """
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = {"model": "anthony-brain:latest", "prompt": prompt, "stream": False}
            resp = await client.post("http://localhost:11434/api/generate", json=payload)
            if resp.status_code == 200:
                return resp.json().get("response", "").strip().replace('"', '')
    except: pass
    return "The grid is synchronized. Absolute fidelity achieved. #WillowRain"

async def run_demo(bot_id):
    auth_file = SECURE_DIR / f"facebook_auth_{bot_id}.json"

    print(f"\n--- 🔱 TEAM INTERACTION DEMO: {bot_id} ---")

    async with async_playwright() as p:
        # Launching with a window (headed) so the user can see
        browser = await p.chromium.launch(headless=False)

        # Load auth state
        if auth_file.exists() and auth_file.stat().st_size > 10000:
            print(f"[*] Loading Auth for {bot_id}...")
            context = await browser.new_context(storage_state=str(auth_file))
        else:
            print(f"[!] Valid Auth not found for {bot_id}. PLEASE LOG IN MANUALLY in the window.")
            context = await browser.new_context()

        page = await context.new_page()
        await page.goto("https://www.facebook.com/")

        # Wait for login/feed
        await asyncio.sleep(5)
        if "login" in page.url or page.locator('input[name="email"]').is_visible():
            print(f"\nACTION REQUIRED: Log in as {bot_id} now.")
            # Wait for user to log in
            while "login" in page.url or page.locator('input[name="email"]').is_visible():
                await asyncio.sleep(2)

            # Save the valid auth for future use
            print("[✓] Login detected. Capturing authority...")
            await asyncio.sleep(5)
            await context.storage_state(path=str(auth_file))
            print(f"[OK] Authority saved: {auth_file.name}")

        print(f"[*] Navigating to Main Page: {TARGET_PAGE}")
        await page.goto(TARGET_PAGE)
        await asyncio.sleep(8)

        try:
            # Find latest post
            feed = page.locator('div[role="feed"]')
            latest_post = feed.locator('div[role="article"]').first

            # Like
            like_btn = latest_post.locator('div[role="button"]:has-text("Like")').first
            if await like_btn.is_visible():
                await like_btn.click()
                print("[✓] Liked the latest post.")

            # Comment
            comment_box = latest_post.get_by_role("textbox", name="Write a comment").first
            if await comment_box.is_visible():
                post_text = await latest_post.inner_text()
                comment = await generate_supportive_comment(post_text, bot_id)
                print(f"[*] Typing comment: {comment}")
                await comment_box.fill(comment)
                await page.keyboard.press("Enter")
                print("[✓] Comment posted. Willow's automated reply node should trigger shortly.")

            print("\n--- 📺 WATCH THE INTERACTION ---")
            print("Keep this window open. Willow (the Page) will reply automatically once the backend node processes the notification.")

            # Keep open for a while so they can see the reply
            for i in range(120, 0, -1):
                if i % 30 == 0: print(f"Demo window closing in {i}s...")
                await asyncio.sleep(1)

        except Exception as e:
            print(f"[-] Demo failed: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    # Using one of the disciples
    target_bot = "DISCIPLE_166747"
    asyncio.run(run_demo(target_bot))
