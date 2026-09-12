import sqlite3
import os

DB_PATH = r"C:\AnthonyAi_Swarm\Obsidian_Carrier.db"

def arm_identity():
    print("🔱 OIS: Arming Director's Master Identity in Obsidian HSS...")
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Ensure Table Exists
    cur.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            msisdn TEXT PRIMARY KEY,
            imsi TEXT,
            data_usage_gb REAL DEFAULT 0.0,
            status TEXT DEFAULT 'ACTIVE'
        )
    """)

    # 2. Insert Director's Fresh Number
    cur.execute("""
        INSERT OR REPLACE INTO subscribers (msisdn, imsi, status)
        VALUES ('+13146764040', '310999166415817', 'ACTIVE')
    """)

    conn.commit()
    conn.close()
    print("✓ SUCCESS: Identity +1 314-676-4040 is now the Root Authority of the Grid.")

if __name__ == "__main__":
    arm_identity()
