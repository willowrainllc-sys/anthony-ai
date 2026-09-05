import httpx
import asyncio
import json

async def trigger_strike():
    url = "http://localhost:8000/api/swarm/ignite"
    print(f"[*] Sending IGNITE signal to {url}...")
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url)
            if resp.status_code == 200:
                print(f"[✓] Success: {resp.json()}")
            else:
                print(f"[-] Error {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"[-] Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(trigger_strike())
