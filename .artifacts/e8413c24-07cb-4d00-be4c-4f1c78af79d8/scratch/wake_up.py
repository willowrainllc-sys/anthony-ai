import sqlite3
import json
import time

DB_PATH = r"C:\AnthonyAi_Swarm\Empire_Vault.db"

def wake_up():
    conn = sqlite3.connect(DB_PATH)
    metadata = json.dumps({"dilation": 1.0, "mode": "ACTIVE", "manual_override": True})
    conn.execute(
        "INSERT INTO empire_events (node, event_type, metadata, timestamp) VALUES (?, ?, ?, ?)",
        ("CORE", "TEMPORAL_SHIFT", metadata, time.time())
    )
    conn.commit()
    conn.close()
    print("SWARM AWAKENED: Dilation reset to 1.0")

if __name__ == "__main__":
    wake_up()
