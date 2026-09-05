# --- ANTHONY MANUAL STRIKE: MAIN FEED v2.0 ---
import asyncio
import os
import sys
import time
from pathlib import Path

# Ensure we can import from local directory
sys.path.append(os.path.dirname(__file__))

from swarm_logger import swarm_log
from mobile_social_agent import MobileSocialAgent as MobileAgent

async def execute_manual_feed_strike():
    agent = MobileAgent()
    if not agent.device_id:
        print("[!] No device detected.")
        return

    swarm_log("🔱 MANUAL STRIKE: Targeting Main Feed...", node="MOBILE")

    # 1. Force Reset Facebook
    agent.shell("am force-stop com.facebook.katana")
    await asyncio.sleep(3)

    # 2. Launch straight to the PAGE ID to avoid navigation drift
    page_id = "1370890679430214"
    swarm_log(f"MANUAL: Forcing Page ID {page_id}...", node="MOBILE")
    # This URI is often the most stable for opening a page's main wall
    agent.shell(f"am start -a android.intent.action.VIEW -d fb://page/{page_id}")
    await asyncio.sleep(12)

    # 3. Check for 'Create' or 'What's on your mind?'
    root = agent.get_ui_dump()
    if root is None:
        swarm_log("[-] UI Dump Failed. Retrying launch...", node="MOBILE")
        agent.shell("input keyevent 3")
        await asyncio.sleep(2)
        agent.shell(f"am start -a android.intent.action.VIEW -d fb://page/{page_id}")
        await asyncio.sleep(10)
        root = agent.get_ui_dump()

    if not root:
        swarm_log("[-] CRITICAL: UI Dump unavailable.", node="MOBILE")
        return

    # THE STRIKE: Find the composer trigger
    trigger = agent.find_node(root, text="What's on your mind?") or \
              agent.find_node(root, text="Create") or \
              agent.find_node(root, content_desc="Create") or \
              agent.find_node(root, content_desc="Write something...")

    if trigger:
        swarm_log(f"MANUAL: Tapping trigger at {trigger}", node="MOBILE")
        agent.tap(trigger[0], trigger[1])
    else:
        swarm_log("MANUAL: Trigger not found in dump. Tapping Page Feed Area [360, 480]", node="MOBILE")
        agent.tap(360, 480) # General area for post boxes on pages

    await asyncio.sleep(8)

    # 4. Attachment (Photo/video)
    root = agent.get_ui_dump()
    media_btn = agent.find_node(root, text="Photo/video") or \
                agent.find_node(root, content_desc="Photo/video") or \
                agent.find_node(root, text="Gallery")

    if not media_btn:
        swarm_log("MANUAL: Media button missing. Tapping lower icon area [100, 1300]", node="MOBILE")
        agent.tap(100, 1300)
    else:
        agent.tap(media_btn[0], media_btn[1])

    await asyncio.sleep(8)

    # 5. Select Newest Item (Top Left of Gallery)
    swarm_log("MANUAL: Selecting top gallery item...", node="MOBILE")
    agent.tap(150, 450)
    await asyncio.sleep(10)

    # 6. Next
    root = agent.get_ui_dump()
    nx = agent.find_node(root, text="Next") or agent.find_node(root, content_desc="Next")
    if nx:
        agent.tap(nx[0], nx[1])
        await asyncio.sleep(6)
    else:
        swarm_log("MANUAL: 'Next' button not found. Tapping Top-Right [650, 100]", node="MOBILE")
        agent.tap(650, 100)
        await asyncio.sleep(6)

    # 7. Post
    swarm_log("MANUAL: Executing final strike...", node="MOBILE")
    agent.tap(650, 100) # Final Post button is almost always Top-Right

    swarm_log("SUCCESS: Manual Feed Strike Dispatched.", node="MOBILE")

if __name__ == "__main__":
    asyncio.run(execute_manual_feed_strike())
