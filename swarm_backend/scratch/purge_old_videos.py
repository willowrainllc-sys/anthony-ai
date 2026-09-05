import os
import glob
import shutil
import sqlite3
from supabase import create_client

def purge_all():
    print("=== PURGING ALL OLD LOCAL VIDEO FILES & CACHE ===")
    dirs_to_clear = [
        r"D:\AnthonyAi_Swarm\Renderings",
        r"C:\AnthonyAi_Swarm\Renderings",
        r"D:\AnthonyAi_Swarm\Secure_Assets\source_videos",
        r"D:\AnthonyAi_Swarm\Temp",
        r"C:\AnthonyAi_Swarm\Temp"
    ]

    for d in dirs_to_clear:
        if os.path.exists(d):
            files = glob.glob(os.path.join(d, "*"))
            print(f"Purging {d} ({len(files)} files)...")
            for f in files:
                try:
                    if os.path.isfile(f):
                        os.remove(f)
                    elif os.path.isdir(f):
                        shutil.rmtree(f)
                except Exception as e:
                    print(f"Error purging {f}: {e}")

    print("=== PURGING ALL OLD DB RECORDS ===")
    for db_path in [r"C:\AnthonyAi_Swarm\Empire_Vault.db", r"D:\AnthonyAi_Swarm\Empire_Vault.db"]:
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cur = conn.cursor()
                cur.execute("DELETE FROM empire_events")
                cur.execute("DELETE FROM swarm_tasks")
                cur.execute("DELETE FROM production_jobs")
                conn.commit()
                print(f"Cleared DB tables in {db_path}")
            except Exception as e:
                print(f"Error clearing DB {db_path}: {e}")

    print("=== PURGING ALL OLD SUPABASE VIDEO ROWS ===")
    SUPABASE_URL = "https://nhurgrrauzuebgrepigg.supabase.co"
    SUPABASE_KEY = "sb_secret_dyQRuiz4y-2W9TN5Mcurbg_QYLYRuc7"
    try:
        s_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        res = s_client.table("videos").select("id").execute()
        count = 0
        for row in res.data:
            s_client.table("videos").delete().eq("id", row["id"]).execute()
            count += 1
        print(f"Purged {count} old video rows from Supabase.")
    except Exception as e:
        print(f"Supabase purge error: {e}")

if __name__ == "__main__":
    purge_all()
