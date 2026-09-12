import asyncio
import os
import uuid
import json
from curl_cffi import requests

async def debug():
    email = f"maestas_debug_{uuid.uuid4().hex[:6]}@obsidian.co"
    payload = {
        "email": email,
        "password": "Alpha_Password123!",
        "coupon_code": "dontpayfull5",
        "referral_code": None
    }

    url = "https://dashboard.obsidian_ingress.com/api/v1/users"

    print(f"Testing signup for {email}...")

    with requests.Session(impersonate="chrome110") as s:
        resp = s.post(
            url,
            json=payload,
            headers={
                "Origin": "https://dashboard.obsidian_ingress.com",
                "Referer": "https://dashboard.obsidian_ingress.com/sign-up",
                "Accept": "application/json, text/plain, */*",
                "Content-Type": "application/json"
            }
        )
        print(f"STATUS: {resp.status_code}")
        print(f"BODY: {resp.text}")

if __name__ == "__main__":
    asyncio.run(debug())
