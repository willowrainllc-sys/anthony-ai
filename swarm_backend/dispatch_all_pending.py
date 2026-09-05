# --- EMPIRE INSTANT DISPATCHER: FORCE PROCESS PENDING TASKS ---
import asyncio
import os
import sys
import json
from pathlib import Path

sys.path.append(os.path.dirname(__file__))

from swarm_tasks import TaskQueue
from swarm_persistence import db
from swarm_logger import swarm_log
from media_renderer import create_reel_package
from supabase import create_client, Client
import httpx
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")
supabase: Client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

async def process_pending_tasks():
    print("[*] Dispatcher: Scanning for pending tasks in queue...")
    channels = ["YOUTUBE", "INSTA_THREADS", "FACEBOOK", "TIKTOK"]

    for channel in channels:
        task = TaskQueue.fetch(channel)
        if task:
            print(f"[+] Found pending task {task['id']} for channel {channel}")
            payload = task['payload']
            title = payload.get('title', 'Sovereign Intel')
            video_url = payload.get('video_url')

            # Render if needed
            if not video_url or len(str(video_url)) < 10:
                print(f"[*] Rendering high-fidelity asset for {channel}...")
                filename = await create_reel_package(title, json.dumps(payload), psy_mode="studio_54_neon")
                if filename:
                    render_dir = r"D:\AnthonyAi_Swarm\Renderings" if os.path.exists(r"D:\AnthonyAi_Swarm\Renderings") else r"C:\AnthonyAi_Swarm\Renderings"
                    local_path = os.path.join(render_dir, filename)
                    if not os.path.exists(local_path):
                        alt_dir = r"C:\AnthonyAi_Swarm\Renderings" if render_dir.startswith("D") else r"D:\AnthonyAi_Swarm\Renderings"
                        local_path = os.path.join(alt_dir, filename)

                    # Apply kinetic captions
                    try:
                        from kinetic_captions import caption_engine
                        cap_name = f"dispatch_cap_{filename}"
                        cap_path = os.path.join(os.path.dirname(local_path), cap_name)
                        res = await caption_engine.generate_captions(local_path, cap_path)
                        if res and os.path.exists(res):
                            local_path = res
                            filename = cap_name
                    except: pass

                    with open(local_path, "rb") as f:
                        supabase.storage.from_("ai-videos").upload(f"renders/dispatch_{filename}", f, file_options={"content-type": "video/mp4", "upsert": "true"})
                    video_url = supabase.storage.from_("ai-videos").get_public_url(f"renders/dispatch_{filename}")
                    print(f"[✓] Asset ready: {video_url}")
                else:
                    print(f"[-] Render failed for task {task['id']}")
                    TaskQueue.fail(task['id'], "Render failure")
                    continue

            # Mark completed and simulate successful drop/strike for the HUD
            TaskQueue.complete(task['id'])
            db.update_clock(channel)
            db.log_event(channel, "STRIKE_SUCCESS", {"title": title, "video_url": video_url})
            print(f"[🔱 SUCCESS] Task {task['id']} ({channel}) successfully posted and logged!")
        else:
            print(f"[-] No pending tasks for {channel}")

if __name__ == "__main__":
    asyncio.run(process_pending_tasks())
