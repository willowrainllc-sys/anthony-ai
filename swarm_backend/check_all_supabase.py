import os
import json
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

def check():
    if not URL or not KEY:
        print("Missing Supabase credentials in .env")
        return

    supabase: Client = create_client(URL, KEY)
    tables = ["videos", "feed_posts", "posts", "ai_videos", "twin_logs"]
    for table in tables:
        try:
            response = supabase.table(table).select("*").order("created_at", desc=True).limit(1).execute()
            if response.data:
                print(f"Table [{table}]: Found {len(response.data)} recent entries.")
                print(json.dumps(response.data[0], indent=2))
            else:
                print(f"Table [{table}] is empty.")
        except Exception as e:
            print(f"Table [{table}] check failed: {e}")

if __name__ == "__main__":
    check()
