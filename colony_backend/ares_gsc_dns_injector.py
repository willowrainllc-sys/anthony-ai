# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES AUTOMATED GSC DNS TXT INJECTOR ---
import asyncio
import os
import httpx
from pathlib import Path
from dotenv import load_dotenv
from colony_logger import colony_log

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

CLOUDFLARE_API_TOKEN = os.getenv("CLOUDFLARE_API_TOKEN")
CLOUDFLARE_ZONE_ID = os.getenv("CLOUDFLARE_ZONE_ID")

async def inject_gsc_txt_record():
    colony_log("ARES GSC DNS: Initializing automated TXT record injection into Cloudflare...", node="SUPREME")

    if not CLOUDFLARE_API_TOKEN or not CLOUDFLARE_ZONE_ID:
        colony_log("[-] Cloudflare API credentials missing in .env", node="SUPREME")
        return False

    url = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records"
    headers = {
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
        "Content-Type": "application/json"
    }

    txt_record = {
        "type": "TXT",
        "name": "@",
        "content": "google-site-verification=XClOSEj0Z07Gy-7TLjlP0VURX67-hqhOEh8HwJr7yD4",
        "ttl": 3600
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(url, headers=headers, json=txt_record)
            if resp.status_code in [200, 201]:
                colony_log("[+] ARES GSC DNS SUCCESS: Google verification TXT record successfully pushed to Cloudflare!", node="SUPREME")
                print("\n" + "="*70)
                print("  [+] ARES GSC TXT RECORD INJECTED VIA CLOUDFLARE API")
                print("  RECORD: TXT @ google-site-verification=XClOSEj0Z07Gy-7TLjlP0VURX67-hqhOEh8HwJr7yD4")
                print("  STATUS: LIVE - Ready for Google Search Console verification")
                print("="*70 + "\n")
                return True
            else:
                colony_log(f"[-] Cloudflare DNS push warning: {resp.status_code} - {resp.text}", node="SUPREME")
                return False
        except Exception as e:
            colony_log(f"[-] Cloudflare DNS push error: {e}", node="SUPREME")
            return False

if __name__ == "__main__":
    asyncio.run(inject_gsc_txt_record())
