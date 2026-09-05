import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def find():
    url = f"{SUPABASE_URL}/rest/v1/"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}"
    }
    try:
        r = requests.get(url, headers=headers)
        data = r.json()
        paths = data.get("paths", {})
        tables = [p.strip("/") for p in paths.keys() if p != "/"]
        print(f"Available tables/endpoints: {tables}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find()
