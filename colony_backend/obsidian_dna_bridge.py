# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN DOMAIN NAME API (DNA) BRIDGE v1.1 ---
import os
import httpx
import json
import base64
import asyncio
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db
from dotenv import load_dotenv

# 🔱 Load environment from root
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

DNA_RESELLER_ID = os.getenv("DNA_RESELLER_ID")
DNA_API_KEY = os.getenv("DNA_API_KEY")
DNA_TEST_KEY = os.getenv("DNA_TEST_KEY")
DNA_ENV = os.getenv("DNA_ENV", "production")

# Endpoint mapping
DNA_URLS = {
    "test": "https://rest-test.domainnameapi.com",
    "production": "https://api.domainresellerapi.com"
}

# Determine which key to use based on environment
ACTIVE_KEY = DNA_API_KEY if DNA_ENV == "production" else DNA_TEST_KEY
BASE_URL = DNA_URLS.get(DNA_ENV, "https://api.domainresellerapi.com")

class ObsidianDnaBridge:
    """
    OBSIDIAN DNA BRIDGE (Atakonline):
    Industrial-grade domain registration and management via ICANN accredited registrar.
    """
    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)
        auth_bytes = f"{DNA_RESELLER_ID}:{ACTIVE_KEY}".encode()
        self.encoded_auth = base64.b64encode(auth_bytes).decode()
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {self.encoded_auth}",
            "Accept": "application/json"
        }

    async def get_account_balance(self):
        """Module 4: Deposit & Balance Ingress."""
        # DNA API often requires a POST for balance or specific endpoints
        url = f"{BASE_URL}/account/balance"
        try:
            resp = await self.client.get(url, headers=self.headers)
            print(f"[*] DNA BALANCE DEBUG: Status {resp.status_code}")
            if resp.status_code == 200:
                return resp.json()
            else:
                print(f"[*] DNA FAIL BODY: {resp.text}")
                return {"error": f"API_{resp.status_code}", "message": resp.text}
        except Exception as e:
            return {"error": "EXCEPTION", "message": str(e)}

    async def register_domain(self, domain: str, period: int = 1):
        """Initiates domain registration protocol with default WHOIS privacy and DNS."""
        colony_log(f"DNA: Initiating registration for [{domain}]...", node="FINANCE")
        url = f"{BASE_URL}/domain/register"

        payload = {
            "domain": domain,
            "period": period,
            "registrant": {"firstName": "Anthony", "lastName": "Maestas", "email": "willow.rain.llc@gmail.com"},
            "ns1": os.getenv("DNA_DNS_1", "tr.apiname.com"),
            "ns2": os.getenv("DNA_DNS_2", "eu.apiname.com"),
            "privacy": True
        }

        try:
            resp = await self.client.post(url, json=payload, headers=self.headers)
            res = resp.json()
            if resp.status_code == 200 and res.get("status") == "success":
                db.log_event("FINANCE", "DOMAIN_DNA_SECURED", {"domain": domain, "status": "ACTIVE"})
                return True, res
            return False, res.get("message", f"DNA Error {resp.status_code}")
        except Exception as e:
            return False, str(e)

dna_bridge = ObsidianDnaBridge()

if __name__ == "__main__":
    async def test():
        print("🔱 TESTING DNA INGRESS (V1.1)...")
        print(f"[*] Reseller ID: {DNA_RESELLER_ID[:6]}...")
        print(f"[*] Base URL: {BASE_URL}")
        res = await dna_bridge.get_account_balance()
        print(json.dumps(res, indent=2))

    asyncio.run(test())
