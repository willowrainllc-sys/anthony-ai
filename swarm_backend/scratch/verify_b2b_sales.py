import sqlite3
import json

def verify():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    rows = conn.execute("SELECT metadata FROM empire_events WHERE event_type='B2B_INVOICE_DISPATCHED' ORDER BY id DESC LIMIT 5").fetchall()

    print("\n=== 🔱 THE AGGREGATOR MODEL: B2B SALES VERIFICATION ===\n")
    for r in rows:
        try:
            m = json.loads(r[0])
            print(f"Client: {m.get('client')}")
            print(f"Volume Sold: {m.get('volume_gb')} GB")
            print(f"Contract Value: ${m.get('total_usd'):,.2f}\n")
        except: pass
    conn.close()

if __name__ == "__main__":
    verify()
