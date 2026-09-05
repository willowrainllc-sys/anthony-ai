import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def check():
    try:
        buckets = supabase.storage.list_buckets()
        print(f"Buckets: {[b.name for b in buckets]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
