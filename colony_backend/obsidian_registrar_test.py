# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN REGISTRAR & SETTLEMENT TESTER v1.0 ---
import httpx
import os
import asyncio
from colony_logger import colony_log

async def test_platform_integrity():
    colony_log("INTEGRITY TEST: Verifying NameSilo and Square bridges...", node="SUPREME")

    # 1. Test NameSilo API
    api_key = "cert_O6RAXSvTTLkhX1TlQcQt9wpA"
    test_domain = "anthonyempire.com"
    url = f"https://www.namesilo.com/api/checkRegisterAvailability?version=1&type=xml&key={api_key}&domains={test_domain}"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url)
            if resp.status_code == 200:
                colony_log(f"✓ NAMESILO BRIDGE: Active. Response received.", node="SUPREME")
            else:
                colony_log(f"[-] NAMESILO BRIDGE: Failed with status {resp.status_code}", node="SUPREME")
    except Exception as e:
        colony_log(f"[-] NAMESILO BRIDGE ERROR: {e}", node="SUPREME")

    # 2. Test Square API (Heuristics)
    square_token = "EAAAl66bPEfbMG8HrWqH0ywIu32fO_19UsXDReI_UvxwSBD6j6Qmat-5AkXcSrnU"
    headers = {"Authorization": f"Bearer {square_token}", "Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://connect.squareup.com/v2/locations", headers=headers)
            if resp.status_code == 200:
                colony_log(f"✓ SQUARE SETTLEMENT: Active. Locations verified.", node="SUPREME")
            else:
                colony_log(f"[-] SQUARE SETTLEMENT: Unauthorized or inactive.", node="SUPREME")
    except Exception as e:
        colony_log(f"[-] SQUARE ERROR: {e}", node="SUPREME")

if __name__ == "__main__":
    asyncio.run(test_platform_integrity())
