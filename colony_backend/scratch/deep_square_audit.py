import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\.env")

TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
BASE_URL = "https://connect.squareup.com/v2"

async def audit_square():
    print("=== 🔱 DEEP SQUARE AUDIT v2: SEARCHING ACROSS ALL LOCATIONS ===")

    headers = {
        "Square-Version": "2024-10-17",
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Audit Locations
        print("[*] Auditing Business Locations...")
        loc_resp = await client.get(f"{BASE_URL}/locations", headers=headers)
        if loc_resp.status_code == 200:
            locations = loc_resp.json().get('locations', [])
            for loc in locations:
                loc_id = loc['id']
                print(f"\n[LOC] {loc['name']} ({loc_id}) - Status: {loc['status']}")

                # 2. Audit Invoices for THIS location
                inv_resp = await client.get(f"{BASE_URL}/invoices?location_id={loc_id}", headers=headers)
                if inv_resp.status_code == 200:
                    invoices = inv_resp.json().get('invoices', [])
                    if not invoices:
                        print(f"  [-] No invoices found for this location.")
                    for inv in invoices:
                        amount = inv.get('payment_requests', [{}])[0].get('computed_amount_money', {}).get('amount', 0) / 100
                        print(f"  [INV] {inv.get('title')} | Amount: ${amount:,.2f} | Status: {inv['status']}")
                else:
                    print(f"  [-] Inv Error: {inv_resp.text}")

if __name__ == "__main__":
    asyncio.run(audit_square())
