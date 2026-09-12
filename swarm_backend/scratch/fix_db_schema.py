import sqlite3
import os

db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Check current columns in ip_pool
    cur.execute("PRAGMA table_info(ip_pool)")
    columns = [col[1] for col in cur.fetchall()]

    if "ip_type" not in columns:
        print("[*] Adding ip_type column to ip_pool...")
        cur.execute("ALTER TABLE ip_pool ADD COLUMN ip_type TEXT DEFAULT 'RESIDENTIAL'")

    if "is_cd_eligible" not in columns:
        print("[*] Adding is_cd_eligible column to ip_pool...")
        cur.execute("ALTER TABLE ip_pool ADD COLUMN is_cd_eligible BOOLEAN DEFAULT 0")

    conn.commit()
    print("✓ DB Schema Fixed.")
    conn.close()
else:
    print("DATABASE_NOT_FOUND")
