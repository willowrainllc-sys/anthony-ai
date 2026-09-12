import sqlite3
import json
import os

def check():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("\n=== 📡 SOCIAL PUBLISHING TASKS AUDIT ===\n")

    print("--- ⏳ NEGOTIATING ---")
    rows = cur.execute("SELECT id, channel, status FROM swarm_tasks WHERE status='NEGOTIATING' LIMIT 5").fetchall()
    for r in rows: print(r)

    print("\n--- ❌ FAILED ---")
    rows = cur.execute("SELECT id, channel, error_log FROM swarm_tasks WHERE status='FAILED' ORDER BY id DESC LIMIT 5").fetchall()
    for r in rows: print(r)

    print("\n--- ✅ COMPLETED ---")
    rows = cur.execute("SELECT id, channel, status FROM swarm_tasks WHERE status='COMPLETED' ORDER BY id DESC LIMIT 5").fetchall()
    for r in rows: print(r)

    conn.close()

if __name__ == "__main__":
    check()
