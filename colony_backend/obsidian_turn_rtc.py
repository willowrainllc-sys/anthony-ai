# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- OBSIDIAN CITY TURN / WebRTC GENERATOR ---
import os
import httpx
import asyncio
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

TURN_TOKEN_ID = os.getenv("CLOUDFLARE_TURN_TOKEN_ID")
TURN_API_TOKEN = os.getenv("CLOUDFLARE_TURN_API_TOKEN")

async def generate_ice_servers():
    """Generates short-lived WebRTC ICE credentials via Cloudflare Calls API."""
    if not TURN_TOKEN_ID or not TURN_API_TOKEN:
        print("[-] TURN credentials missing in .env")
        return None

    url = f"https://rtc.live.cloudflare.com/v1/turn/keys/{TURN_TOKEN_ID}/credentials/generate-ice-servers"
    headers = {
        "Authorization": f"Bearer {TURN_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {"ttl": 86400} # Valid for 24 hours

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(url, headers=headers, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                print("[+] ICE Servers successfully generated via Cloudflare TURN")
                return data.get("iceServers", [])
            else:
                print(f"[-] Cloudflare TURN API Error: {resp.status_code} - {resp.text}")
                return None
        except Exception as e:
            print(f"[-] Cloudflare TURN API Request Failed: {e}")
            return None

if __name__ == "__main__":
    ice_servers = asyncio.run(generate_ice_servers())
    if ice_servers:
        print(f"\n{ice_servers}\n")
