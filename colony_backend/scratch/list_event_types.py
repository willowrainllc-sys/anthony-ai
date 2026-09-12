import sqlite3
import os

db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT event_type FROM empire_events")
    types = cur.fetchall()
    print("EVENT_TYPES:")
    for t in types:
        print(f"  - {t[0]}")
    conn.close()
else:
    print("DATABASE_NOT_FOUND")
