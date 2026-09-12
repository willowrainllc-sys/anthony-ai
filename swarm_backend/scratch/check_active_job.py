import sqlite3
import json

def check():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    rows = conn.execute('SELECT job_id, status, progress, current_stage FROM production_jobs ORDER BY created_at DESC LIMIT 5').fetchall()
    print("--- RECENT JOBS ---")
    for r in rows:
        print(f"JOB: {r[0]} | Status: {r[1]} | Progress: {r[2]}% | Stage: {r[3]}")
    conn.close()

if __name__ == "__main__":
    check()
