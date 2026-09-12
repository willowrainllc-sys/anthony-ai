# --- WILLOW RAIN ENTERPRISES: CLOUD FEED SEEDER v1.0 ---
import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

def seed():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        print("Missing credentials")
        return

    supabase: Client = create_client(url, key)

    print(f"Seeding cloud feed for: {url}")

    video = {
        "title": "[SUPREME] OBSIDIAN CLOUD ACTIVE: SYSTEM INITIALIZED",
        "description": "Willow Rain Company LLC has successfully activated the Master Cloud Database. All systems are OBSIDIAN.",
        "video_url": "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        "thumbnail_url": "https://images.unsplash.com/photo-1545143333-14387679366a?q=80&w=600",
        "creator": "Obsidian AI",
        "category": "For you",
        "views": "1.2M",
        "posted": "Just Now"
    }

    try:
        res = supabase.table("videos").insert(video).execute()
        print(" SUCCESS: Cloud feed seeded with initial Obsidian Drop.")
    except Exception as e:
        print(f"[-] SEED ERROR: {e}")

if __name__ == "__main__":
    seed()
