import os
import sqlite3
import time
from pathlib import Path

DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'
RENDER_DIR = Path(r'D:\AnthonyAi_Swarm\Renderings')

def register_assets():
    print("=== 🔱 CONTENT HUB: FORCING VIDEO REGISTRATION ===")

    if not os.path.exists(DB_PATH):
        print(f"[-] DB Missing at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)

    # 1. Scan the Renderings folder for finished MP4s
    videos = list(RENDER_DIR.glob("*.mp4"))
    print(f"[*] Found {len(videos)} physical MP4 assets.")

    # 2. Force register them into production_jobs as 'READY'
    for v in videos:
        # Ignore zero-byte files
        if v.stat().st_size == 0: continue

        job_id = f"FORCE-{v.stem[-6:]}"
        title = v.stem.replace("_", " ").title()

        conn.execute("""
            INSERT OR REPLACE INTO production_jobs
            (job_id, title, final_video_path, status, current_stage, updated_at)
            VALUES (?, ?, ?, 'READY', 'COMPLETED', ?)
        """, (job_id, title, str(v), time.time()))
        print(f"  [✓] REGISTERED: {title}")

    conn.commit()
    conn.close()
    print("\n✓ SUCCESS: Production queue is ARMED. Ready for Social Push.")

if __name__ == "__main__":
    register_assets()
