# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES VERCEL DNS TXT/CNAME INJECTOR ---
import asyncio
import os
import httpx
from pathlib import Path
from dotenv import load_dotenv
from colony_logger import colony_log

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

VERCEL_TOKEN = os.getenv("VERCEL_TOKEN")
VERCEL_TEAM_ID = os.getenv("VERCEL_TEAM_ID")
DOMAIN = "obsidian.city"

async def inject_vercel_dns():
    colony_log("ARES VERCEL DNS: Initializing automated DNS record insertion via Vercel API...", node="SUPREME")

    if not VERCEL_TOKEN:
        colony_log("[-] VERCEL_TOKEN missing in .env", node="SUPREME")
        return False

    headers = {
        "Authorization": f"Bearer {VERCEL_TOKEN}",
        "Content-Type": "application/json"
    }

    params = {}
    if VERCEL_TEAM_ID:
        params["teamId"] = VERCEL_TEAM_ID

    url = f"https://api.vercel.com/v4/domains/{DOMAIN}/records"

    payload = {
        "name": "abguofx4u23e",
        "type": "CNAME",
        "value": "gv-7xgdmluzv5z62a.dv.googlehosted.com",
        "ttl": 60
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(url, headers=headers, params=params, json=payload)
            if resp.status_code in [200, 201]:
                colony_log("[+] ARES VERCEL DNS SUCCESS: Google CNAME record successfully added to Vercel DNS!", node="SUPREME")
                print("\n" + "="*70)
                print("  [+] ARES VERCEL DNS CNAME INJECTOR SUCCESS")
                print("  RECORD: CNAME abguofx4u23e -> gv-7xgdmluzv5z62a.dv.googlehosted.com")
                print("  STATUS: LIVE - Ready for Google Search Console verification")
                print("="*70 + "\n")
                return True
            else:
                colony_log(f"[-] Vercel DNS API warning: {resp.status_code} - {resp.text}", node="SUPREME")
                return False
        except Exception as e:
            colony_log(f"[-] Vercel DNS API error: {e}", node="SUPREME")
            return False

if __name__ == "__main__":
    asyncio.run(inject_vercel_dns())
