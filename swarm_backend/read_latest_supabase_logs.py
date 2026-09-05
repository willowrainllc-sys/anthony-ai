import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

URL = os.getenv("SUPABASE_URL")
KEY = os.getenv("SUPABASE_KEY")

def read_latest():
    if not URL or not KEY:
        print("Missing Supabase credentials")
        return

    supabase: Client = create_client(URL, KEY)
    try:
        response = supabase.table("twin_logs").select("*").order("id", desc=True).limit(10).execute()
        for log in reversed(response.data):
            print(f"[{log['id']}] {log['user_prompt']} -> {log['ai_response']}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    read_latest()
