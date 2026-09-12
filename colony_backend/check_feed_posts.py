import os
import json
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check():
    print("--- CHECKING FEED_POSTS TABLE ---")
    try:
        response = supabase.table("feed_posts").select("*").execute()
        data = response.data
        print(f"Total items: {len(data)}")
        for i, item in enumerate(data[:5]):
            print(f"\nItem {i+1}:")
            print(f"Title: {item.get('title')}")
            print(f"Category: {item.get('category')}")
            print(f"Video URL: {item.get('video_url')}")
            print(f"Thumbnail URL: {item.get('thumbnail_url')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
