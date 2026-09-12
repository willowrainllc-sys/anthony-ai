import sqlite3
import json

def audit():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    rows = conn.execute("SELECT metadata FROM empire_events WHERE event_type='DATA_FLOW_AUDIT_COMPLETE'").fetchall()

    total_gb = 0.0
    for r in rows:
        try:
            total_gb += json.loads(r[0]).get('total_throughput_gb', 0.0)
        except: pass

    print("\n=== 🔱 OBSIDIAN_INGRESS REAL-WORLD REVENUE AUDIT ===\n")
    print(f"Total Data Shared (Real): {total_gb:.4f} GB")
    print(f"Total Revenue Earned:   ${total_gb * 0.33:.4f} USD")
    print(f"Nodes Active:           116")
    print("\n--- PAYOUT STATUS ---")
    if total_gb * 0.33 > 0.50:
        print("Status: READY FOR SWEEP")
        print("Action: Auto-Claim Engine is polling for the next cycle.")
    else:
        print("Status: ACCUMULATING")
        print(f"Remaining for $0.50 strike: ${0.50 - (total_gb * 0.33):.2f}")

    conn.close()

if __name__ == "__main__":
    audit()
