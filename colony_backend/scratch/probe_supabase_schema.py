import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()

async def probe_tables():
    url = os.getenv('SUPABASE_URL')
    key = os.getenv('SUPABASE_KEY')
    headers = {'apikey': key, 'Authorization': f'Bearer {key}'}

    tables = ['videos', 'active_feed_registry', 'content_profiles', 'twin_logs', 'feed_posts', 'production_batches', 'projects']

    async with httpx.AsyncClient() as client:
        print(f"Probing project: {url}")
        for table in tables:
            try:
                resp = await client.get(f'{url}/rest/v1/{table}?select=count', headers=headers)
                if resp.status_code == 200:
                    print(f"[✓] Table '{table}' EXISTS")
                elif resp.status_code == 404:
                    print(f"[-] Table '{table}' NOT FOUND")
                else:
                    print(f"[!] Table '{table}' returned error: {resp.status_code} - {resp.text}")
            except Exception as e:
                print(f"[!] Error probing '{table}': {e}")

if __name__ == "__main__":
    asyncio.run(probe_tables())
