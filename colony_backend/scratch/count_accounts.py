import sqlite3
import os

db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) FROM empire_events WHERE event_type='ACCOUNT_CREATED'")
    count = cur.fetchone()[0]
    print(f"TOTAL_ACCOUNTS_CREATED: {count}")
    conn.close()
else:
    print("DATABASE_NOT_FOUND")
