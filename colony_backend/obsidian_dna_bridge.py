# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN DOMAIN NAME API (DNA) BRIDGE v1.0 ---
import os
import httpx
import json
import base64
import asyncio
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

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
    1. AVAILABILITY: Real-time multi-TLD check.
    2. REGISTRATION: Full automated provisioning burst.
    3. MANAGEMENT: DNS, WHOIS, and Renewal handshakes.
    4. AUTH: Uses Basic Auth (ResellerID:APIKey).
    """
    def __init__(self):
        self.auth = httpx.BasicAuth(DNA_RESELLER_ID, ACTIVE_KEY)
        self.client = httpx.AsyncClient(timeout=30.0, auth=self.auth)
        self.common_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    async def check_availability(self, domain: str):
        """Checks if a domain is available for registration."""
        colony_log(f"DNA: Querying availability for [{domain}]...", node="FINANCE")
        url = f"{BASE_URL}/domain/check"
        payload = {"domain": domain}

        try:
            resp = await self.client.post(url, json=payload, headers=self.common_headers)
            print(f"[*] DNA DEBUG: Status {resp.status_code}")
            if resp.status_code != 200:
                print(f"[*] DNA DEBUG: Body {resp.text[:500]}")
                return {"error": f"API Error {resp.status_code}"}

            data = resp.json()
            is_available = data.get("isAvailable", False)
            price = data.get("price", 0.0)
            return {
                "domain": domain,
                "available": is_available,
                "price": price,
                "provider": "DNA"
            }
        except Exception as e:
            colony_log(f"[-] DNA CHECK ERROR: {e}", node="FINANCE")
            return {"error": str(e)}

    async def register_domain(self, domain: str, period: int = 1):
        """Initiates domain registration protocol with default WHOIS privacy and DNS."""
        colony_log(f"DNA: Initiating registration for [{domain}]...", node="FINANCE")
        url = f"{BASE_URL}/domain/register"

        # 🔱 Default Configuration from Godfather's Settings
        payload = {
            "domain": domain,
            "period": period,
            "registrant": {"firstName": "Anthony", "lastName": "Maestas", "email": "willow.rain.llc@gmail.com"},
            "ns1": os.getenv("DNA_DNS_1", "tr.apiname.com"),
            "ns2": os.getenv("DNA_DNS_2", "eu.apiname.com"),
            "privacy": True # Armored WHOIS
        }

        try:
            resp = await self.client.post(url, json=payload, headers=self.common_headers)
            res = resp.json()
            if res.get("status") == "success":
                db.log_event("FINANCE", "DOMAIN_DNA_SECURED", {"domain": domain, "status": "ACTIVE"})
                return True, res
            return False, res.get("message", "Unknown DNA Error")
        except Exception as e:
            return False, str(e)

    async def get_account_balance(self):
        """Module 4: Deposit & Balance Ingress."""
        url = f"{BASE_URL}/account/balance"
        try:
            resp = await self.client.get(url, headers=self.common_headers)
            print(f"[*] DNA BALANCE DEBUG: Status {resp.status_code}")
            print(f"[*] DNA BALANCE DEBUG: Body {resp.text}")
            return resp.json()
        except Exception as e:
            print(f"[-] DNA BALANCE ERROR: {e}")
            return {"error": str(e)}

dna_bridge = ObsidianDnaBridge()

if __name__ == "__main__":
    async def test():
        print("🔱 TESTING DNA INGRESS...")
        res = await dna_bridge.get_account_balance()
        print(json.dumps(res, indent=2))

    asyncio.run(test())
