# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- VERCEL SERVERLESS API GATEWAY FOR OBSIDIAN CITY ---
import time
import json
import random
import os
import urllib.parse
import httpx
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler

# 🔱 WHOLESALE & DATABASE BRIDGES
NAMESILO_KEY = os.environ.get("NAMESILO_API_KEY", "cert_O6RAXSvTTLkhX1TlQcQt9wpA")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "qWDIVVoR27MYlXxWil4roFhwgBTVovgX5GnXqpEtbzHIxj2rNAu1APFd")

# 🔱 SOVEREIGN STATE DATABASE (All 50 States)
STATES_DB = {
    "AL": {"name": "Alabama", "fee": 200, "time": "2-3 weeks"},
    "AK": {"name": "Alaska", "fee": 250, "time": "10-15 days"},
    "AZ": {"name": "Arizona", "fee": 50, "time": "7-10 days"},
    "AR": {"name": "Arkansas", "fee": 45, "time": "1-2 days"},
    "CA": {"name": "California", "fee": 70, "time": "5-7 days"},
    "CO": {"name": "Colorado", "fee": 50, "time": "Instant"},
    "CT": {"name": "Connecticut", "fee": 120, "time": "3-5 days"},
    "DE": {"name": "Delaware", "fee": 90, "time": "2-3 days"},
    "FL": {"name": "Florida", "fee": 125, "time": "2-3 days"},
    "GA": {"name": "Georgia", "fee": 100, "time": "5-7 days"},
    "HI": {"name": "Hawaii", "fee": 50, "time": "3-5 days"},
    "ID": {"name": "Idaho", "fee": 100, "time": "7-10 days"},
    "IL": {"name": "Illinois", "fee": 150, "time": "10-15 days"},
    "IN": {"name": "Indiana", "fee": 95, "time": "Instant"},
    "IA": {"name": "Iowa", "fee": 50, "time": "1-2 days"},
    "KS": {"name": "Kansas", "fee": 160, "time": "Instant"},
    "KY": {"name": "Kentucky", "fee": 40, "time": "1-2 days"},
    "LA": {"name": "Louisiana", "fee": 100, "time": "3-5 days"},
    "ME": {"name": "Maine", "fee": 175, "time": "5-10 days"},
    "MD": {"name": "Maryland", "fee": 100, "time": "4-6 weeks"},
    "MA": {"name": "Massachusetts", "fee": 500, "time": "1-2 days"},
    "MI": {"name": "Michigan", "fee": 50, "time": "10-15 days"},
    "MN": {"name": "Minnesota", "fee": 135, "time": "3-5 days"},
    "MS": {"name": "Mississippi", "fee": 50, "time": "Instant"},
    "MO": {"name": "Missouri", "fee": 50, "time": "Instant"},
    "MT": {"name": "Montana", "fee": 70, "time": "7-10 days"},
    "NE": {"name": "Nebraska", "fee": 100, "time": "2-3 days"},
    "NV": {"name": "Nevada", "fee": 425, "time": "1-2 days"},
    "NH": {"name": "New Hampshire", "fee": 100, "time": "3-5 days"},
    "NJ": {"name": "New Jersey", "fee": 125, "time": "Instant"},
    "NM": {"name": "New Mexico", "fee": 50, "time": "10-15 days"},
    "NY": {"name": "New York", "fee": 200, "time": "7-10 days"},
    "NC": {"name": "North Carolina", "fee": 125, "time": "3-5 days"},
    "ND": {"name": "North Dakota", "fee": 135, "time": "Instant"},
    "OH": {"name": "Ohio", "fee": 99, "time": "3-5 days"},
    "OK": {"name": "Oklahoma", "fee": 100, "time": "Instant"},
    "OR": {"name": "Oregon", "fee": 100, "time": "Instant"},
    "PA": {"name": "Pennsylvania", "fee": 125, "time": "2-3 weeks"},
    "RI": {"name": "Rhode Island", "fee": 150, "time": "Instant"},
    "SC": {"name": "South Carolina", "fee": 110, "time": "Instant"},
    "SD": {"name": "South Dakota", "fee": 150, "time": "Instant"},
    "TN": {"name": "Tennessee", "fee": 300, "time": "Instant"},
    "TX": {"name": "Texas", "fee": 300, "time": "2-3 days"},
    "UT": {"name": "Utah", "fee": 70, "time": "24 hours"},
    "VT": {"name": "Vermont", "fee": 125, "time": "3-5 days"},
    "VA": {"name": "Virginia", "fee": 100, "time": "Instant"},
    "WA": {"name": "Washington", "fee": 200, "time": "2-3 days"},
    "WV": {"name": "West Virginia", "fee": 100, "time": "5-10 days"},
    "WI": {"name": "Wisconsin", "fee": 130, "time": "Instant"},
    "WY": {"name": "Wyoming", "fee": 100, "time": "Instant"}
}

SESSIONS = {}
ORDERS = {}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        now = time.time()
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if "/api/domains/search" in path:
            raw_q = query_params.get("domain", [""])[0] or query_params.get("q", [""])[0]
            if not raw_q: raw_q = "mybrand"
            q = raw_q.lower().split('.')[0].replace(/[^a-z0-9]/g, '')
            if not q: q = "mybrand"

            # Simulated wholesale availability check
            tlds = [".com", ".ai", ".io", ".city", ".rocks", ".net", ".org"]
            results = []
            for tld in tlds:
                results.append({
                    "domain": f"{q}{tld}",
                    "available": random.random() > 0.3,
                    "price": 14.70 if tld == ".com" else 59.99 if tld == ".ai" else 9.99,
                    "tag": "Wholesale" if tld == ".com" else "Recommended"
                })
            payload = {"query": q, "results": results, "timestamp": now}
            self.wfile.write(json.dumps(payload).encode('utf-8'))

        elif "/api/llc/state-info" in path:
            state_code = query_params.get("state", ["AR"])[0].upper()
            state_data = STATES_DB.get(state_code, STATES_DB["AR"])
            payload = {
                "success": True,
                "state": state_data,
                "obsidian_fee": 39.00,
                "agent_fee": 125.00
            }
            self.wfile.write(json.dumps(payload).encode('utf-8'))

        elif "/api/orders/status" in path:
            email = query_params.get("email", [""])[0]
            user_orders = [o for o in ORDERS.values() if o["email"] == email]
            self.wfile.write(json.dumps({"success": True, "orders": user_orders}).encode('utf-8'))

        elif "/api/aura/video" in path:
            payload = {"success": True, "url": "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a56763a14e9&profile_id=175"}
            self.wfile.write(json.dumps(payload).encode('utf-8'))

        else:
            self.wfile.write(json.dumps({"status": "SUCCESS"}).encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        payload = json.loads(post_data) if post_data else {}
        path = self.path

        if "/api/settle/authorize" in path:
            # 🔱 TRANSACTION PIPELINE: Settle & Queue
            email = payload.get("email")
            item_type = payload.get("type")
            amount = payload.get("amount")
            txid = f"TX-{int(time.time())}-{random.randint(1000, 9999)}"

            order = {
                "id": txid,
                "email": email,
                "type": item_type,
                "amount": amount,
                "status": "PROCESSING",
                "llc_details": payload.get("llc_details"),
                "timestamp": time.time()
            }
            ORDERS[txid] = order

            # Simulate background automation (n8n/Python worker)
            # 1. Generate Articles of Organization PDF (Placeholder)
            # 2. Trigger Domain Purchase (GoDaddy API v3 placeholder)
            # 3. Queue Physical Mail (Lob.com placeholder)

            response = {"success": True, "txid": txid, "status": "AUTHORIZED"}
            self.wfile.write(json.dumps(response).encode('utf-8'))

        elif "/api/auth/signin" in path:
            email = payload.get("email", "user@example.com")
            sid = f"sess_{int(time.time())}"
            SESSIONS[sid] = {"email": email}
            self.wfile.write(json.dumps({"success": True, "session_id": sid, "email": email}).encode('utf-8'))

        else:
            self.wfile.write(json.dumps({"status": "SUCCESS"}).encode('utf-8'))
