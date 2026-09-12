# --- OBSIDIAN GLOBAL: SOCIAL HUB FORCE PUSH v2.0 (HARDENED) ---
import sqlite3
import json
import os
import uuid
import time
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

# Configuration
DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def force_push_all_ready_videos():
    """
    FORCE PUSH v2.0:
    Finds all successfully rendered videos in the vault and pushes them
    to YouTube, Facebook, Instagram, and Threads automatically.
    """
    if not os.path.exists(DB_PATH):
        swarm_log(f"[-] SOCIAL_PUSH: Database missing at {DB_PATH}", node="SOCIAL_HUB")
        return

    swarm_log("[SUPREME] SOCIAL_PUSH: Unlocking automatic social net dispatch...", node="SOCIAL_HUB")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Find all successful strike events with video paths
    # We also check production_jobs for status='READY'
    jobs = cur.execute("SELECT job_id, title, final_video_path FROM production_jobs WHERE status='READY'").fetchall()

    pushed_count = 0
    platforms = ["YOUTUBE", "FACEBOOK", "INSTA_THREADS", "TIKTOK", "X"]

    for job_id, title, video_path in jobs:
        try:
            if video_path and os.path.exists(video_path):
                # 2. Push to all platforms
                for hub in platforms:
                    payload = {
                        "title": title or f"Obsidian Documentary [{job_id}]",
                        "description": f"{title}\n\nBuilt by AnthonyChristopher Maestas. #Obsidian #Wealth #Innovation",
                        "video_url": video_path,
                        "job_id": job_id,
                        "timestamp": time.time()
                    }
                    # Idempotency to prevent duplicates
                    idemp_key = f"force_push_{hub}_{job_id}"

                    success = db.push_task(hub, payload, priority=20, idempotency_key=idemp_key)
                    if success:
                        pushed_count += 1
        except Exception as e:
            swarm_log(f"[-] SOCIAL_PUSH Error on {job_id}: {e}", node="SOCIAL_HUB")

    conn.close()
    swarm_log(f" SOCIAL_PUSH SUCCESS: Dispatched {pushed_count} strike tasks across the hub.", node="SOCIAL_HUB")
    return pushed_count

if __name__ == "__main__":
    force_push_all_ready_videos()
