import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def verify_location():
    token = os.getenv('SQUARE_ACCESS_TOKEN')
    loc_id = os.getenv('SQUARE_LOCATION_ID')
    url = f'https://connect.squareup.com/v2/locations/{loc_id}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Square-Version': '2024-10-17',
        'Content-Type': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        resp = await client.get(url, headers=headers)
        if resp.status_code == 200:
            loc = resp.json().get('location', {})
            print(f"VERIFIED_NAME: {loc.get('name')}")
            print(f"VERIFIED_ID: {loc.get('id')}")
            print(f"VERIFIED_ADDRESS: {loc.get('address', {}).get('address_line_1')}, {loc.get('address', {}).get('locality')}")
        else:
            print(f"ERROR: {resp.status_code} - {resp.text}")

if __name__ == "__main__":
    asyncio.run(verify_location())
