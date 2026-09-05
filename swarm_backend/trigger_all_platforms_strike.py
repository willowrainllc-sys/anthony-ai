# --- EMPIRE MASTER STRIKE: ALL PLATFORMS (MIND SERVER API) ---
import asyncio
import httpx
import json
from swarm_logger import swarm_log

async def trigger_mind_server_strike():
    url = "http://localhost:8000/api/swarm/strike"
    payload = {
        "platforms": ["YOUTUBE", "INSTA_THREADS", "FACEBOOK", "TIKTOK"],
        "title": "SOVEREIGN HIGH-FIDELITY SPECTRUM STRIKE",
        "description": "Brand new 2026 production. Studio 54 neon decadence, Unreal Engine 5.4 Lumen lighting. Zero archival footage."
    }

    print("[*] Dispatching Master Strike to Mind Server Service...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                print(f"[✓] Mind Server Strike Queued Successfully!")
                print(json.dumps(data, indent=2))
            else:
                print(f"[-] Mind Server Error ({resp.status_code}): {resp.text}")
    except Exception as e:
        print(f"[-] Failed to connect to Mind Server at {url}: {e}")
        print("[*] Make sure the Mind Server is running (run_mind_server.bat)")

if __name__ == "__main__":
    asyncio.run(trigger_mind_server_strike())
