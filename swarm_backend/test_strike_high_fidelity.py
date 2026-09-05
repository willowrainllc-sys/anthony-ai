# --- ANTHONY TEST STRIKE: HIGH-FIDELITY MODERNA v1.0 ---
import asyncio
import os
import sys
import time
from pathlib import Path

# Ensure we can import from local directory
sys.path.append(os.path.dirname(__file__))

from swarm_logger import swarm_log
from mobile_social_agent import MobileSocialAgent as MobileAgent

# MISSION PAYLOAD
TARGET_VIDEO = Path(r"C:\AnthonyAi_Swarm\Renderings\remix_hyper_stock_9573667f.mp4")
PAGE_ID = "1370890679430214" # Willow Rain Company LLC

async def execute_moderna_strike():
    agent = MobileAgent()
    if not agent.device_id:
        print("[!] No device detected.")
        return

    swarm_log(f"🔱 TEST STRIKE: Moderna High-Fidelity mission for {TARGET_VIDEO.name}...", node="MOBILE")

    # 1. PUSH
    if not TARGET_VIDEO.exists():
        print(f"[!] Payload missing: {TARGET_VIDEO}")
        return

    remote_path = agent.push_file(str(TARGET_VIDEO))
    agent.shell(f"am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file://{remote_path}")
    await asyncio.sleep(2)

    # 2. ANCHOR & LAUNCH
    agent.shell("am force-stop com.facebook.katana")
    await asyncio.sleep(2)
    # Launch straight to page
    agent.shell(f"am start -a android.intent.action.VIEW -d fb://page/{PAGE_ID}")
    await asyncio.sleep(12)

    # 3. VERIFY ANCHOR & SWITCH
    root = agent.get_ui_dump()
    switcher = agent.find_node(root, text="Switch") or agent.find_node(root, content_desc="Switch")
    if switcher:
        swarm_log("MANUAL: Switching to Willow Rain profile...", node="MOBILE")
        agent.tap(switcher[0], switcher[1])
        await asyncio.sleep(12)
        root = agent.get_ui_dump()

    # 4. COMPOSER
    trigger = agent.find_node(root, text="What's on your mind?") or \
              agent.find_node(root, text="Create") or \
              agent.find_node(root, content_desc="Write something...")

    if trigger:
        agent.tap(trigger[0], trigger[1])
    else:
        agent.tap(360, 450)
    await asyncio.sleep(6)

    # 5. ATTACHMENT
    root = agent.get_ui_dump()
    media_btn = agent.find_node(root, text="Photo/video") or \
                agent.find_node(root, content_desc="Photo/video") or \
                agent.find_node(root, text="Gallery")

    if media_btn:
        agent.tap(media_btn[0], media_btn[1])
        await asyncio.sleep(8)

        # Select Top-Left (Newest)
        agent.tap(150, 450)
        await asyncio.sleep(10)

        # Next
        agent.tap(650, 100) # Fast Next
        await asyncio.sleep(8)

        # 6. CAPTION (Moderna Niche / Matching Topic)
        # Niche: Heavy Hauling / Industrial Muscle
        caption = (
            "🔱 MODERNA INDUSTRIAL SERIES: EPISODE 04 🔱\n\n"
            "Witness the pure power of heavy hauling. Synchronized movement in the urban grid. "
            "High-fidelity production for the Alpha Spectrum.\n\n"
            "#HeavyMachinery #IndustrialMuscle #HighFidelity #WillowRain #AlphaGrid #Sovereignty"
        )

        agent.tap(360, 400)
        await asyncio.sleep(2)
        agent.type_text(caption)
        await asyncio.sleep(2)
        agent.shell("input keyevent 4")
        await asyncio.sleep(4)

        # 7. FINAL DISPATCH
        agent.tap(650, 100)
        swarm_log("SUCCESS: Moderna High-Fidelity Strike Dispatched.", node="MOBILE")

        # Cleanup
        await asyncio.sleep(15)
        agent.delete_remote_file(remote_path)

if __name__ == "__main__":
    asyncio.run(execute_moderna_strike())
