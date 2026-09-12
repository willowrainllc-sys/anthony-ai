import os
import asyncio
import sys
from pathlib import Path
from dotenv import load_dotenv

# Setup paths
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
sys.path.append(str(ROOT / "colony_backend"))
load_dotenv(ROOT / ".env")

from square_checkout_gateway import square_gateway

async def strike():
    print("🔱 SQUARE STRIKE: Creating real $9,000 invoice for AI Lab...")

    # Targeting a high-aura lead
    res = await square_gateway.create_and_publish_invoice(
        client_name="St. Louis AI Research Lab",
        email="procurement@stlouis-ai.org",
        amount_usd=9000.0,
        description="Wholesale Obsidian Matrix Access: 5,000 GB High-Aura Residential Ingress"
    )

    if res.get("status") == "success":
        print(f"🎯 SUCCESS: Invoice {res['invoice_id']} is now NEGOTIATING in your Square Dashboard.")
        print(f"🔗 Public URL: {res['url']}")
    else:
        print(f"[-] FAILED: {res.get('message')}")

if __name__ == "__main__":
    asyncio.run(strike())
