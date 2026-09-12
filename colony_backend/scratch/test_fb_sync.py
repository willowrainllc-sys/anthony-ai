import asyncio
import os
import httpx
from facebook_rotator import fb_rotator

async def test_fb():
    print("[*] Probing Facebook Page Authority...")
    identity = await fb_rotator.get_identity_async()
    if not identity:
        print("[-] FAILED: No Facebook identity found in .env or Grid.")
        return

    print(f"[✓] identity Found: {identity['name']} (ID: {identity['id']})")
    print(f"[*] Token Sample: {identity['token'][:10]}...")

    # Test API connection
    url = f"https://graph.facebook.com/v21.0/{identity['id']}?fields=name,is_published,verification_status&access_token={identity['token']}"
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code == 200:
            print(f"[✓] API Access Verified: {resp.json()}")
        else:
            print(f"[-] API Error: {resp.text}")

if __name__ == "__main__":
    asyncio.run(test_fb())
