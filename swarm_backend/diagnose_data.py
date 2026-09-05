import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def audit():
    tables_to_try = ["videos", "feed_posts", "ai_feed_items", "posts"]
    print("--- SEARCHING FOR FEED TABLES ---")

    for table in tables_to_try:
        try:
            print(f"Checking table: {table}...", end=" ")
            response = supabase.table(table).select("*").limit(1).execute()
            print(f"SUCCESS! Found table with {len(response.data)} sample row.")
            if response.data:
                print(f"Columns: {list(response.data[0].keys())}")
        except Exception as e:
            if "PGRST205" in str(e):
                print("NOT FOUND")
            else:
                print(f"ERROR: {e}")

if __name__ == "__main__":
    audit()
