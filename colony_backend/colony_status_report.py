# --- WILLOW RAIN COMPANY LLC: COLONY STATUS REPORT FOR ANTHONY ---
import sqlite3
import time
import json

def get_report():
    conn = sqlite3.connect(r'C:\ObsidianAi_Colony\Empire_Vault.db')
    cur = conn.cursor()

    print("\n=== [SUPREME] COLONY INTELLIGENCE REPORT: FOR ANTHONY CHRISTOPHER MAESTAS ===\n")

    # 1. Daemon heartbeats
    print("---  DAEMON HEARTBEATS ---")
    rows = cur.execute("SELECT name, status, last_heartbeat FROM daemon_registry").fetchall()
    for name, status, last in rows:
        diff = int(time.time() - last)
        print(f"[{name}] Status: {status} | Pulse: {diff}s ago")

    # 2. Revenue pipeline
    print("\n--- [CASH] REVENUE PIPELINE ---")
    rows = cur.execute("SELECT event_type, metadata FROM empire_events WHERE event_type LIKE '%SUCCESS%' OR event_type LIKE '%CREATED%' ORDER BY id DESC LIMIT 5").fetchall()
    for evt, meta_str in rows:
        meta = json.loads(meta_str)
        val = meta.get('total_usd', meta.get('amount_usd', meta.get('revenue', '0.00')))
        print(f"[{evt}] Value: ${val}")

    # 3. Colony stats
    print("\n---  HONEY COMB STATS ---")
    rows = cur.execute("SELECT COUNT(*) FROM virtual_nodes WHERE status='GATHERING'").fetchone()
    print(f"Active Gathering Nodes: {rows[0]}")

    conn.close()

if __name__ == "__main__":
    get_report()
