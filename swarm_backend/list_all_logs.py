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
        response = supabase.table("twin_logs").select("*").execute()
        for log in response.data:
            print(f"[{log['id']}] {log['user_prompt']} -> {log['ai_response'][:100]}...")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
