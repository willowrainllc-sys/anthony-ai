import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def create():
    try:
        print("Creating bucket 'ai-videos'...")
        supabase.storage.create_bucket("ai-videos", options={"public": True})
        print("Bucket created successfully.")
    except Exception as e:
        print(f"Error creating bucket: {e}")

if __name__ == "__main__":
    create()
