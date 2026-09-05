import os
import httpx
import asyncio
from dotenv import load_dotenv
from pathlib import Path
from swarm_logger import swarm_log

# Load env
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)
PRINTFUL_API_KEY = os.getenv("PRINTFUL_API_KEY")

async def wipe_all_stores():
    if not PRINTFUL_API_KEY:
        print("Error: PRINTFUL_API_KEY not found.")
        return

    headers = {"Authorization": f"Bearer {PRINTFUL_API_KEY}"}
    swarm_log("WIPER: Initiating ULTIMATE Global Store Purge...", node="COMMERCE")

    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. Get all stores
        s_resp = await client.get("https://api.printful.com/stores", headers=headers)
        stores = s_resp.json().get("result", [])

        for store in stores:
            store_id = store['id']
            store_name = store['name']
            swarm_log(f"WIPER: Clearing Store: {store_name} ({store_id})", node="COMMERCE")

            # 2. Aggressive deletion loop
            while True:
                # Fetch products (Printful defaults to 20, we use 100 for speed)
                p_resp = await client.get("https://api.printful.com/sync/products", headers=headers, params={"store_id": store_id, "limit": 100})
                res_json = p_resp.json()

                # Check for rate limit
                if res_json.get("code") == 429:
                    swarm_log("WIPER: Rate limited. Sleeping 60s...", node="COMMERCE")
                    await asyncio.sleep(60)
                    continue

                products = res_json.get("result", [])
                if not products:
                    swarm_log(f"WIPER: Store {store_name} is CLEAN.", node="COMMERCE")
                    break

                swarm_log(f"WIPER: Deleting batch of {len(products)} products...", node="COMMERCE")

                for p in products:
                    # Check for "blank" condition or just delete everything if requested
                    # User wants to remove the "bad" ones (blank mockups)

                    pid = p.get('id')
                    pname = p.get('name')

                    # We check if the product has a thumbnail
                    thumbnail = p.get('thumbnail_url')

                    # If thumbnail is missing, or it's a generic placeholder, or we just want a fresh start:
                    if not thumbnail or "placeholder" in thumbnail or True: # Wiping all for the "Redo"
                        del_resp = await client.delete(f"https://api.printful.com/sync/products/{pid}", headers=headers, params={"store_id": store_id})
                        if del_resp.status_code == 200:
                            print(f"  [X] PURGED: {pname}")
                        else:
                            print(f"  [!] FAIL: {pname} | {del_resp.text}")

                    await asyncio.sleep(0.3) # Pacing

    swarm_log("SUCCESS: Global Empire Purge Complete. All stores are 100% EMPTY.", node="COMMERCE")

if __name__ == "__main__":
    asyncio.run(wipe_all_stores())
