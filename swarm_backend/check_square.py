import os
import httpx
import asyncio
from dotenv import load_dotenv
from pathlib import Path

# Load env from root
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SQUARE_TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")

async def verify_square_connection():
    """Verifies that the Square production keys are active and linked to the business."""
    print("[*] [FINANCIAL HUB] Verifying Square Production Credentials...")

    url = "https://connect.squareup.com/v2/locations"
    headers = {
        "Square-Version": "2024-10-17",
        "Authorization": f"Bearer {SQUARE_TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                locations = resp.json().get("locations", [])
                if locations:
                    biz_name = locations[0].get("business_name", "Willow Rain Company LLC")
                    print(f"[[*]] SQUARE SECURE: Linked to Business Node: {biz_name}")
                    print(f"[OK] Financial Gateway ready for Facebook Monetization deposits.")
                else:
                    print("[!] SQUARE LINKED: But no business locations found.")
            else:
                print(f"[-] SQUARE CONNECTION WEAK: {resp.status_code} | {resp.text}")
        except Exception as e:
            print(f"[!] Financial Gateway Error: {e}")

if __name__ == "__main__":
    if not SQUARE_TOKEN:
        print("[-] SQUARE_ACCESS_TOKEN not found in .env")
    else:
        asyncio.run(verify_square_connection())
