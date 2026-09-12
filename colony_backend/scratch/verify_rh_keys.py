import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def verify():
    api_key = os.getenv("ROBINHOOD_API_KEY")
    print(f"Testing Robinhood API Key: {api_key[:10]}...")

    # Official Robinhood Cloud API check (Crypto account endpoint)
    url = "https://api.robinhood.com/api/v1/crypto/accounts/"
    headers = {
        "x-api-key": api_key,
        "Content-Type": "application/json"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(url, headers=headers)
            print(f"RESPONSE CODE: {resp.status_code}")
            if resp.status_code == 200:
                print("✓ REAL WORLD CONNECTED")
                print(resp.json())
            else:
                print(f"[-] UNAUTHORIZED: {resp.text[:200]}")
    except Exception as e:
        print(f"[-] CONNECTION ERROR: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
