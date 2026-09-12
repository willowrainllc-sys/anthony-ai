import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

PRINTFUL_API_KEY = os.getenv("PRINTFUL_API_KEY")

async def verify_printful():
    print("[*] [PRINTFUL DIAGNOSTIC] Verifying API Connection...")

    if not PRINTFUL_API_KEY:
        print("[!] ERROR: PRINTFUL_API_KEY missing in .env")
        return

    headers = {"Authorization": f"Bearer {PRINTFUL_API_KEY}"}

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            # 1. Verify Authentication & Fetch Stores
            print("[*] Step 1: Fetching Stores...")
            store_resp = await client.get("https://api.printful.com/stores", headers=headers)

            if store_resp.status_code == 200:
                stores = store_resp.json().get("result", [])
                if not stores:
                    print("[!] No stores found linked to this API key.")
                    return

                store = stores[0]
                store_id = store.get("id")
                print(f"[[*]] Found Store: {store.get('name')} (ID: {store_id})")

                # 2. Fetch Products for this Store
                print(f"[*] Step 2: Fetching Product Catalog for Store {store_id}...")
                product_resp = await client.get(f"https://api.printful.com/sync/products?store_id={store_id}", headers=headers)

                if product_resp.status_code == 200:
                    products = product_resp.json().get("result", [])
                    print(f"[[*]] Connection Verified. Found {len(products)} synced products.")
                    for p in products[:5]:
                        print(f"  - {p.get('name')} (ID: {p.get('id')})")
                    if len(products) > 5:
                        print(f"  ... and {len(products)-5} more.")
                else:
                    print(f"[!] Product Fetch Failed: {product_resp.status_code} | {product_resp.text}")
            else:
                print(f"[!] Authentication Failed: {store_resp.status_code} | {store_resp.text}")

        except Exception as e:
            print(f"[!] Connection Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify_printful())
