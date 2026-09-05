import asyncio
import os
import sys
import traceback
from pathlib import Path
from mobile_frontend_dispatcher import FrontendDispatcher
from swarm_logger import swarm_log

async def trigger():
    print("--- MANUAL FRONTEND TRIGGER ENGAGED ---")
    try:
        dispatcher = FrontendDispatcher()
        # Force a scan and post
        success = await dispatcher.post_latest_render()
        if success:
            print("[SUCCESS] Mission payload dispatched to physical phone.")
        else:
            print("[INFO] No new payload found or already posted.")
    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(trigger())
