import sqlite3
import json
import os

db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'

def audit():
    if not os.path.exists(db_path):
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT metadata FROM empire_events WHERE event_type='RENDER_FAILED' ORDER BY id DESC LIMIT 5").fetchall()

    print("=== 🔱 RENDER FAILURE AUDIT ===\n")
    for r in rows:
        try:
            data = json.loads(r[0])
            print(f"Job: {data.get('job_id')} | Error: {data.get('error')[:200]}")
        except: pass
    conn.close()

if __name__ == "__main__":
    audit()
