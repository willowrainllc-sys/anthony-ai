# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY DATABASE SYNCHRONIZER v1.0 ---
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 🔱 Initialize Environment
load_dotenv()
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

class ObsidianDatabase:
    """
    OBSIDIAN CITY PERSISTENT DATABASE BRIDGE:
    Uses Supabase to synchronize user sessions, digital asset ownership,
    and platform data separation between Director (Anthony) and Customers.
    """
    def __init__(self):
        self.active = False
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
                self.active = True
                print("✓ OBSIDIAN DATABASE: Supabase Link Active.")
            except Exception as e:
                print(f"[-] DATABASE ERROR: {e}")
        else:
            print("[-] DATABASE WARNING: Supabase Credentials missing. Falling back to Local Vault.")

    def save_session(self, sid, email, metadata=None):
        if not self.active: return False
        try:
            data = {"id": sid, "email": email, "metadata": metadata, "last_active": "now()"}
            self.client.table("sessions").upsert(data).execute()
            return True
        except Exception: return False

    def record_purchase(self, email, item_type, amount, txid):
        if not self.active: return False
        try:
            data = {"email": email, "item": item_type, "amount": amount, "txid": txid, "created_at": "now()"}
            self.client.table("purchases").insert(data).execute()
            return True
        except Exception: return False

    def get_purchases(self, email):
        """Retrieves user order history from Supabase."""
        if not self.active: return []
        try:
            res = self.client.table("purchases").select("*").eq("email", email).order("created_at", desc=True).execute()
            return res.data
        except Exception: return []

    def is_director(self, email):
        # 🔱 SUPREME OVERRIDE: Identify the Boss (Godfather)
        directors = ["google_user@obsidian.city", "willow.rain.llc@gmail.com"]
        email_low = email.lower()
        return any(d == email_low for d in directors) or email_low.startswith("anthony")

# 🔱 Global Instance
db_bridge = ObsidianDatabase()
