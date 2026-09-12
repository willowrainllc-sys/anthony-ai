import sqlite3
import json
import os

def inspect():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("\n=== 🔱 LIVE TRANSACTION & REVENUE LEDGER ===\n")

    # 1. Payouts
    q = "SELECT node, event_type, metadata FROM empire_events WHERE event_type IN ('RELAY_TRAFFIC_COMMISSION_DISPATCHED', 'DISCIPLE_REWARD_CLAIMED', 'CLUSTER_YIELD_DISPATCHED', 'STABLECOIN_SQUARE_SYNCED') ORDER BY id DESC LIMIT 10"
    rows = cur.execute(q).fetchall()
    for node, ev_type, meta in rows:
        data = json.loads(meta)
        amt = data.get('daily_yield_usd') or data.get('earned_usd_value') or data.get('amount_usd') or 'N/A'
        dest = data.get('bank_payout_destination') or data.get('delivery_destination') or 'Vault'
        print(f"[{node}] {ev_type}: ${amt} -> {dest}")

    # 2. Supervisor
    print("\n--- MASTER SUPERVISOR AUDIT TRACES ---")
    traces = cur.execute("SELECT worker_name, action_type, quality_score, status FROM supervisor_traces ORDER BY timestamp DESC LIMIT 5").fetchall()
    for worker, action, score, status in traces:
        print(f"[{worker}] {action}: Score {score}/100 | {status}")

    conn.close()

if __name__ == "__main__":
    inspect()
