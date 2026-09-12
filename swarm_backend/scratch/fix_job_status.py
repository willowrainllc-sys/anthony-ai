import sqlite3
import os

def fix():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("Fixing job statuses...")
    cur.execute("UPDATE production_jobs SET status='QUEUED' WHERE status='IDEATION'")
    print(f"Updated {cur.rowcount} jobs.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    fix()
