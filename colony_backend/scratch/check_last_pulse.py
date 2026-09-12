import sqlite3
import json

def check():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    row = conn.execute("SELECT event_type, metadata, timestamp FROM empire_events WHERE event_type LIKE 'MISSION_LOCKDOWN%' ORDER BY id DESC LIMIT 1").fetchone()
    if row:
        print(f"LAST PULSE: {row[0]} at {row[2]}")
    else:
        print("No mission pulses found.")
    conn.close()

if __name__ == "__main__":
    check()
