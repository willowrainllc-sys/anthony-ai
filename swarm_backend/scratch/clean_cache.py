import os
import glob
import shutil
import sqlite3
from supabase import create_client

def run_cleanup():
    print("=== PURGING TEMP & CACHE DIRS ===")
    temp_dirs = [
        r"C:\AnthonyAi_Swarm\Temp",
        r"D:\AnthonyAi_Swarm\Temp",
        r"D:\AnthonyAi_Swarm\Secure_Assets\source_videos"
    ]

    for td in temp_dirs:
        if os.path.exists(td):
            files = glob.glob(os.path.join(td, "*"))
            print(f"Cleaning {td} ({len(files)} files)...")
            for f in files:
                try:
                    if os.path.isfile(f): os.remove(f)
                    elif os.path.isdir(f): shutil.rmtree(f)
                except Exception as e:
                    print(f"Err cleaning {f}: {e}")

    print("=== PURGING STALE DB EVENTS & TASKS ===")
    for db_path in [r"C:\AnthonyAi_Swarm\Empire_Vault.db", r"D:\AnthonyAi_Swarm\Empire_Vault.db"]:
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute("DELETE FROM empire_events WHERE metadata LIKE '%127.0.0.1%' OR metadata LIKE '%file://%'")
                cur.execute("DELETE FROM swarm_tasks WHERE status='FAILED'")
                conn.commit()
                print(f"Cleaned DB: {db_path}")
            except Exception as e:
                print(f"DB clean error on {db_path}: {e}")

    print("=== PURGING BROKEN SUPABASE ROWS ===")
    SUPABASE_URL = "https://nhurgrrauzuebgrepigg.supabase.co"
    SUPABASE_KEY = "sb_secret_dyQRuiz4y-2W9TN5Mcurbg_QYLYRuc7"
    try:
        s_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        res = s_client.table("videos").select("id, video_url").execute()
        for row in res.data:
            v_url = str(row.get("video_url", ""))
            if not v_url.startswith("http") or "file:" in v_url or "127.0.0.1" in v_url:
                s_client.table("videos").delete().eq("id", row["id"]).execute()
                print(f"Deleted invalid video row {row['id']}")
        print("Supabase cleanup complete.")
    except Exception as e:
        print(f"Supabase error: {e}")

if __name__ == "__main__":
    run_cleanup()
