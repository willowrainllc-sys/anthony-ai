# --- OBSIDIAN GLOBAL: SQUARE PRODUCTION GATEWAY v8.0 (HARDENED) ---
import os
import json
import uuid
import time
import httpx
import asyncio
from pathlib import Path
from swarm_logger import swarm_log

SQUARE_TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
# Corrected for 'willow rain Co'
SQUARE_LOC = "L1H0AHZQR8T4G"

class SquareCheckoutGateway:
    """
    SQUARE PRODUCTION GATEWAY v8.0:
    Physically publishes REAL Invoices to the Director's Square Dashboard.
    """
    def __init__(self):
        self.access_token = SQUARE_TOKEN
        self.base_url = "https://connect.squareup.com/v2"

    async def create_digital_product_checkout(self, title: str, price_usd: float) -> dict:
        """Alias for creating an invoice meant for digital products/marketplaces to fix the crash."""
        swarm_log(f"SQUARE: Initiating Digital Product Checkout for [{title}]...", node="SQUARE")

        # We spoof a generic client name for anonymous digital checkouts
        mock_client = f"Digital Buyer {uuid.uuid4().hex[:4]}"
        mock_email = f"buyer_{uuid.uuid4().hex[:6]}@obsidian-global.io"

        result = await self.create_and_publish_invoice(
            client_name=mock_client,
            email=mock_email,
            amount_usd=price_usd,
            description=title
        )

        return {
            "status": result.get("status"),
            "checkout_url": result.get("url", "https://square.link/fallback")
        }

    async def create_and_publish_invoice(self, client_name: str, email: str, amount_usd: float, description: str):
        swarm_log(f"SQUARE: Initiating Real Invoice Strike for [{client_name}]...", node="SQUARE")

        if not self.access_token:
            return {"status": "error", "message": "Token Missing"}

        headers = {
            "Square-Version": "2024-10-17",
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # 1. Provision Customer
                c_body = {
                    "idempotency_key": uuid.uuid4().hex,
                    "given_name": client_name.split()[0],
                    "family_name": client_name.split()[-1] if len(client_name.split()) > 1 else "Buyer",
                    "email_address": email,
                    "company_name": client_name
                }
                c_resp = await client.post(f"{self.base_url}/customers", json=c_body, headers=headers)
                customer_id = c_resp.json()['customer']['id'] if c_resp.status_code in [200, 201] else None
                if not customer_id: return {"status": "error", "message": "Customer Creation Fail"}

                # 2. Create Order
                order_payload = {
                    "idempotency_key": uuid.uuid4().hex,
                    "order": {
                        "location_id": SQUARE_LOC,
                        "line_items": [{
                            "name": description,
                            "quantity": "1",
                            "base_price_money": {"amount": int(amount_usd * 100), "currency": "USD"}
                        }]
                    }
                }
                o_resp = await client.post(f"{self.base_url}/orders", json=order_payload, headers=headers)
                if o_resp.status_code != 200: return {"status": "error", "message": f"Order Fail: {o_resp.text}"}
                order_id = o_resp.json()['order']['id']

                # 3. Create Draft Invoice
                inv_payload = {
                    "idempotency_key": uuid.uuid4().hex,
                    "invoice": {
                        "order_id": order_id,
                        "location_id": SQUARE_LOC,
                        "primary_recipient": {"customer_id": customer_id},
                        "payment_requests": [{
                            "request_type": "BALANCE",
                            "due_date": time.strftime("%Y-%m-%d"),
                        }],
                        "delivery_method": "EMAIL",
                        "title": f"Obsidian Global: {client_name}",
                        "accepted_payment_methods": {
                            "bank_account": True,
                            "card": True,
                            "square_gift_card": True
                        }
                    }
                }
                i_resp = await client.post(f"{self.base_url}/invoices", json=inv_payload, headers=headers)
                if i_resp.status_code not in [200, 201]: return {"status": "error", "message": f"Invoice Draft Fail: {i_resp.text}"}
                invoice_id = i_resp.json()['invoice']['id']
                version = i_resp.json()['invoice']['version']

                # 4. PUBLISH
                p_payload = {"idempotency_key": uuid.uuid4().hex, "version": version}
                p_resp = await client.post(f"{self.base_url}/invoices/{invoice_id}/publish", json=p_payload, headers=headers)

                if p_resp.status_code == 200:
                    swarm_log(f"✓ SQUARE SUCCESS: Invoice published to [willow rain Co].", node="SQUARE")
                    return {"status": "success", "invoice_id": invoice_id, "url": p_resp.json()['invoice'].get('public_url')}

                return {"status": "error", "message": "Publish Fail"}
        except Exception as e:
            swarm_log(f"[-] SQUARE CRITICAL: {e}", node="SQUARE")
            return {"status": "error", "message": str(e)}

square_gateway = SquareCheckoutGateway()
