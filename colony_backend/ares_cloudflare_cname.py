# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES CLOUDFLARE CNAME INJECTOR ---
import os
import httpx
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")

def add_cname():
    if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID:
        print("[-] Cloudflare tokens missing")
        return False

    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "type": "CNAME",
        "name": "832bf47af17add6ff8b04481a9ecd7f2",
        "content": "verify.bing.com",
        "proxied": False,
        "ttl": 3600
    }

    try:
        resp = httpx.post(url, headers=headers, json=payload, timeout=30.0)
        print(f"Cloudflare Response: {resp.status_code} - {resp.text}")
        return resp.status_code in [200, 201]
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    add_cname()
