import os
import asyncio
import httpx
import uuid
import time
from dotenv import load_dotenv

load_dotenv(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\.env")

TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
CORRECT_LOC_ID = "L1H0AHZQR8T4G"
BASE_URL = "https://connect.squareup.com/v2"

async def fix_strike():
    print("=== 🔱 SQUARE LOCATION CORRECTION: ATTEMPT 2 ===")

    headers = {
        "Square-Version": "2024-10-17",
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Provision/Find Customer
        print("[*] Ensuring Buyer Identity exists...")
        c_body = {
            "idempotency_key": uuid.uuid4().hex,
            "given_name": "Missouri",
            "family_name": "Procurement",
            "email_address": "procurement@mo-ai.org",
            "company_name": "St. Louis AI Research Group"
        }
        c_resp = await client.post(f"{BASE_URL}/customers", json=c_body, headers=headers)
        customer_id = c_resp.json()['customer']['id'] if c_resp.status_code in [200, 201] else "3T675J7J0X20BWV7JGMWQCGJ3M"

        # 2. Create the Order
        print(f"[*] Anchoring $9,000.00 Order at [willow rain Co]...")
        o_body = {
            "idempotency_key": uuid.uuid4().hex,
            "order": {
                "location_id": CORRECT_LOC_ID,
                "line_items": [{
                    "name": "Wholesale Obsidian Matrix: 5,000 GB High-Aura Ingress",
                    "quantity": "1",
                    "base_price_money": {"amount": 900000, "currency": "USD"}
                }]
            }
        }
        o_resp = await client.post(f"{BASE_URL}/orders", json=o_body, headers=headers)
        if o_resp.status_code != 200:
            print(f"[-] Order Fail: {o_resp.text}")
            return
        order_id = o_resp.json()['order']['id']

        # 3. Create the Invoice (With required Payment Methods)
        print("[*] Drafting Industrial Invoice for correct location...")
        i_body = {
            "idempotency_key": uuid.uuid4().hex,
            "invoice": {
                "order_id": order_id,
                "location_id": CORRECT_LOC_ID,
                "primary_recipient": {"customer_id": customer_id},
                "payment_requests": [{
                    "request_type": "BALANCE",
                    "due_date": time.strftime("%Y-%m-%d")
                }],
                "delivery_method": "EMAIL",
                "title": "OBSIDIAN GLOBAL: Wholesale Ingress Retainer",
                "accepted_payment_methods": {
                    "bank_account": True,
                    "card": True,
                    "square_gift_card": True
                }
            }
        }
        i_resp = await client.post(f"{BASE_URL}/invoices", json=i_body, headers=headers)
        if i_resp.status_code in [200, 201]:
            invoice = i_resp.json()['invoice']
            # 4. PUBLISH
            p_body = {"idempotency_key": uuid.uuid4().hex, "version": invoice['version']}
            p_resp = await client.post(f"{BASE_URL}/invoices/{invoice['id']}/publish", json=p_body, headers=headers)

            if p_resp.status_code == 200:
                print(f"\n🎯 SUCCESS: $9,000.00 INVOICE IS NEGOTIATING AT [willow rain Co].")
                print(f"🔗 Public Link: {p_resp.json()['invoice'].get('public_url')}")
            else:
                print(f"[-] Publish Fail: {p_resp.text}")
        else:
            print(f"[-] Invoice Fail: {i_resp.text}")

if __name__ == "__main__":
    asyncio.run(fix_strike())
