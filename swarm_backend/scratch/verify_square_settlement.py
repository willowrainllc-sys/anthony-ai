import os
import asyncio
import httpx
from dotenv import load_dotenv

load_dotenv(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\.env")

TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
LOC_ID = os.getenv("SQUARE_LOCATION_ID")
BASE_URL = "https://connect.squareup.com/v2"

async def check_settlement():
    print("🔱 SQUARE AUDIT: Checking for 'Negotiating' Invoices via HTTPX...")

    headers = {
        "Square-Version": "2024-10-17",
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            # Need to provide location_id
            resp = await client.get(f"{BASE_URL}/invoices?location_id={LOC_ID}", headers=headers)
            if resp.status_code == 200:
                invoices = resp.json().get('invoices', [])
                if not invoices:
                    print("\n[!] ALERT: 0 Invoices found. The system has NOT published the $9,000 strike yet.")
                    return

                for inv in invoices:
                    status = inv.get('status')
                    title = inv.get('title', 'No Title')
                    amount = inv.get('payment_requests', [{}])[0].get('computed_amount_money', {}).get('amount', 0) / 100
                    print(f"  [INVOICE] {title} | Amount: ${amount:,.2f} | Status: {status}")
            else:
                print(f"[-] ERROR: {resp.status_code} - {resp.text}")
        except Exception as e:
            print(f"[-] EXCEPTION: {e}")

if __name__ == "__main__":
    asyncio.run(check_settlement())
