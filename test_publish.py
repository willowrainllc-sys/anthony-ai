import os
import httpx
from dotenv import load_dotenv

load_dotenv()

FB_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")
PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")

async def test():
    if not FB_TOKEN or not PAGE_ID:
        print(f"Error: Missing credentials. Token: {bool(FB_TOKEN)}, PageID: {PAGE_ID}")
        return

    video_url = "https://nhurgrrauzuebgrepigg.supabase.co/storage/v1/object/public/ai-videos/news/swarm_137c879b.mp4"
    url = f"https://graph.facebook.com/v19.0/{PAGE_ID}/videos"

    data = {
        "file_url": video_url,
        "description": "Test post from Anthony AI Swarm",
        "access_token": FB_TOKEN
    }

    async with httpx.AsyncClient() as client:
        print(f"Publishing to: {url}")
        resp = await client.post(url, data=data)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
