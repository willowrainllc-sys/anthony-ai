import sqlite3
import os

def fix():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("Cleaning database...")
    # Reset all jobs that aren't READY or SUCCESS to QUEUED
    cur.execute("UPDATE production_jobs SET status='QUEUED' WHERE status != 'READY'")
    print(f"Reset {cur.rowcount} production jobs.")

    # Reset swarm tasks
    cur.execute("UPDATE swarm_tasks SET status='NEGOTIATING' WHERE status != 'COMPLETED'")
    print(f"Reset {cur.rowcount} swarm tasks.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix()
