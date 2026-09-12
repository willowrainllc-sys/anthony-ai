import sqlite3
import json
import os
import time

def check():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("--- NEGOTIATING JOBS ---")
    rows = cur.execute("SELECT job_id, status, progress, current_stage FROM production_jobs WHERE status != 'READY'").fetchall()
    for r in rows:
        print(r)

    print("\n--- NEGOTIATING SOCIAL TASKS ---")
    rows = cur.execute("SELECT id, channel, status FROM swarm_tasks WHERE status = 'NEGOTIATING'").fetchall()
    for r in rows:
        print(r)

    conn.close()

if __name__ == "__main__":
    check()
