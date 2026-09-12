import os
import asyncio
import httpx
import uuid
import time
from dotenv import load_dotenv

load_dotenv(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\.env")

TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
LOC_ID = os.getenv("SQUARE_LOCATION_ID")
BASE_URL = "https://connect.squareup.com/v2"

async def force_strike():
    print("=== 🔱 FORCE 9K SETTLEMENT: INITIATING PHYSICAL STRIKE ===")

    headers = {
        "Square-Version": "2024-10-17",
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Create a Customer Profile for the Buyer
        print("[*] Provisioning AI Lab Procurement Identity...")
        c_body = {
            "idempotency_key": uuid.uuid4().hex,
            "given_name": "Missouri",
            "family_name": "Procurement",
            "email_address": "procurement@mo-ai.org",
            "company_name": "St. Louis AI Research Group"
        }
        c_resp = await client.post(f"{BASE_URL}/customers", json=c_body, headers=headers)
        if c_resp.status_code not in [200, 201]:
            print(f"[-] Customer Fail: {c_resp.text}")
            return
        customer_id = c_resp.json()['customer']['id']

        # 2. Create the Order
        print("[*] Anchoring $9,000.00 Order...")
        o_body = {
            "idempotency_key": uuid.uuid4().hex,
            "order": {
                "location_id": LOC_ID,
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

        # 3. Create the Invoice (DRAFT)
        print("[*] Drafting Industrial Invoice...")
        i_body = {
            "idempotency_key": uuid.uuid4().hex,
            "invoice": {
                "order_id": order_id,
                "primary_recipient": {"customer_id": customer_id},
                "payment_requests": [{
                    "request_type": "BALANCE",
                    "due_date": time.strftime("%Y-%m-%d")
                }],
                "delivery_method": "EMAIL",
                "title": "OBSIDIAN GLOBAL: Wholesale Ingress Retainer",
                "accepted_payment_methods": {"bank_account": True, "card": True, "square_gift_card": True}
            }
        }
        i_resp = await client.post(f"{BASE_URL}/invoices", json=i_body, headers=headers)
        if i_resp.status_code not in [200, 201]:
            print(f"[-] Invoice Draft Fail: {i_resp.text}")
            return
        invoice_id = i_resp.json()['invoice']['id']
        version = i_resp.json()['invoice']['version']

        # 4. PUBLISH THE INVOICE (This makes it "Negotiating")
        print("[*] PUBLISHING STRIKE TO SQUARE...")
        p_body = {"idempotency_key": uuid.uuid4().hex, "version": version}
        p_resp = await client.post(f"{BASE_URL}/invoices/{invoice_id}/publish", json=p_body, headers=headers)

        if p_resp.status_code == 200:
            print("\n🎯 SUCCESS: $9,000.00 INVOICE IS NOW NEGOTIATING.")
            print(f"🔗 Public Link: {p_resp.json()['invoice'].get('public_url')}")
        else:
            print(f"[-] Final Publish Fail: {p_resp.text}")

if __name__ == "__main__":
    asyncio.run(force_strike())
