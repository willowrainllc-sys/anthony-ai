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
    try:
        response = supabase.table("videos").select("*").execute()
        print(f"Connection Successful. Found {len(response.data)} videos.")
        if response.data:
            print("Latest Video Sample:")
            print(json.dumps(response.data[0], indent=2))
        else:
            print("Videos table is empty.")
    except Exception as e:
        print(f"Supabase Check Failed: {e}")

if __name__ == "__main__":
    check()
