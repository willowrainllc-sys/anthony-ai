import sqlite3
import json
import os

def find():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    print("\n=== 🔱 REAL PAYMENT LINKS READY FOR CASH-IN ===\n")

    # Check for B2B Invoices
    rows = conn.execute("SELECT metadata FROM empire_events WHERE event_type LIKE '%INVOICE%' OR event_type LIKE '%SALE%' ORDER BY id DESC").fetchall()

    if not rows:
        print("No real links found in the logs yet.")
    else:
        for r in rows:
            try:
                meta = json.loads(r[0])
                client = meta.get('client', meta.get('buyer', 'Retail Product'))
                url = meta.get('checkout_url')
                amount = meta.get('total_usd', meta.get('fee', 'NEGOTIATING'))
                if url:
                    print(f"💰 OFFER: {client}")
                    print(f"   VALUE: ${amount}")
                    print(f"   LINK:  {url}\n")
            except: continue

    conn.close()
    print("NOTE: Money ONLY enters your bank when a human clicks these links and completes the checkout.")

if __name__ == "__main__":
    find()
