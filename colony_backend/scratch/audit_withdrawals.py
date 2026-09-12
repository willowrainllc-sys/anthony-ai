import sqlite3
import json
import os

def audit():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        print("Database not found at " + db_path)
        return

    conn = sqlite3.connect(db_path)
    print("\n=== 🔱 WITHDRAWAL & CASHOUT AUDIT ===\n")

    # Check for all withdrawal related events
    rows = conn.execute("SELECT event_type, metadata, timestamp FROM empire_events WHERE event_type LIKE '%WITHDRAWAL%' OR event_type LIKE '%CASHOUT%' OR event_type LIKE '%EXCHANGE%' ORDER BY id DESC LIMIT 20").fetchall()

    if not rows:
        print("No withdrawal or cashout events found in the registry.")
    else:
        for r in rows:
            event_type = r[0]
            metadata = json.loads(r[1])
            ts = r[2]
            print(f"[{event_type}] Time: {ts}")
            print(f"   Data: {metadata}\n")

    conn.close()

if __name__ == "__main__":
    audit()
