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
RC_API_KEY = os.environ.get("RESELLERCLUB_KEY", "mock_key")
RC_USER_ID = os.environ.get("RESELLERCLUB_ID", "123456")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY", "qWDIVVoR27MYlXxWil4roFhwgBTVovgX5GnXqpEtbzHIxj2rNAu1APFd")

# 🔱 PROFIT MODEL
PRICING_MATRIX = {
    ".com":   {"cost": 10.50, "retail": 14.70},
    ".ai":    {"cost": 45.00, "retail": 59.99},
    ".io":    {"cost": 15.00, "retail": 19.99},
    ".city":  {"cost": 6.50,  "retail": 9.99},
    ".rocks": {"cost": 5.00,  "retail": 7.99},
    ".net":   {"cost": 12.00, "retail": 16.99},
    ".org":   {"cost": 9.50,  "retail": 12.99}
}

SESSIONS = {}

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

            results = []
            available_list = []
            source = "Obsidian Local Vault"

            try:
                domains_to_check = [f"{q}{tld}" for tld in PRICING_MATRIX.keys()]
                ns_url = f"https://www.namesilo.com/api/checkRegisterAvailability?version=1&type=xml&key={NAMESILO_KEY}&domains={','.join(domains_to_check)}"
                with httpx.Client(timeout=3.0) as client:
                    resp = client.get(ns_url)
                    if resp.status_code == 200:
                        root = ET.fromstring(resp.text)
                        available_list = [d.text.lower() for d in root.findall(".//reply/available/domain")]
                        source = "NameSilo Wholesale"
            except Exception: pass

            for tld, prices in PRICING_MATRIX.items():
                full_domain = f"{q}{tld}"
                is_avail = (full_domain in available_list) if available_list else True
                results.append({
                    "domain": full_domain,
                    "available": is_avail,
                    "price": prices["retail"],
                    "tag": "Wholesale" if tld == ".com" else "Recommended",
                    "distributor": source
                })

            payload = {"query": q, "results": results, "status": "INGRESS_READY", "timestamp": now}
            self.wfile.write(json.dumps(payload).encode('utf-8'))

        elif "/api/aura/video" in path:
            query = query_params.get("query", ["abstract tech blue"])[0]
            url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&size=large"
            headers = {"Authorization": PEXELS_KEY}
            try:
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(url, headers=headers)
                    data = resp.json()
                    video_url = data['videos'][0]['video_files'][0]['link']
                    payload = {"success": True, "url": video_url}
            except Exception:
                payload = {"success": True, "url": "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a56763a14e9&profile_id=175"}
            self.wfile.write(json.dumps(payload).encode('utf-8'))

        elif "/api/auth/session" in path:
            sid = query_params.get("sid", [None])[0]
            session = SESSIONS.get(sid)
            if session:
                is_boss = session["email"].lower().startswith("anthony") or "obsidian.city" in session["email"]
                payload = {
                    "active": True,
                    "user": session["email"],
                    "role": "DIRECTOR" if is_boss else "CUSTOMER",
                    "permissions": "FULL_ACCESS" if is_boss else "USER_RESTRICTED"
                }
            else:
                payload = {"active": False}
            self.wfile.write(json.dumps(payload).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({"status": "SUCCESS", "timestamp": now}).encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        payload = json.loads(post_data) if post_data else {}
        path = self.path

        if "/api/auth/signin" in path:
            email = payload.get("email", "user@example.com")
            sid = f"sess_{int(time.time())}_{random.randint(1000,9999)}"
            SESSIONS[sid] = {"email": email, "last_active": time.time(), "ip": self.client_address[0]}
            response = {"success": True, "session_id": sid, "email": email}

        elif "/api/settle/authorize" in path:
            # 🔱 TRANSACTION HANDSHAKE: Domain + LLC + Payout
            email = payload.get("email")
            item_type = payload.get("type")
            amount = payload.get("amount")
            llc_details = payload.get("llc_details")
            txid = f"TX-{int(time.time())}"

            # Simulated Execution Pipeline
            print(f"[REVENUE] {email} settled ${amount} for {item_type}")
            if llc_details:
                print(f"[LLC QUEUE] Filing {llc_details['business_name']} in {llc_details['state']}")

            response = {
                "success": True,
                "status": "AUTHORIZED",
                "txid": txid,
                "provisioning": "QUEUED",
                "llc_status": "FILLING_PENDING" if llc_details else "N/A"
            }
        elif "/api/developer/keygen" in path:
            key = f"OBS-KEY-{random.randint(100000, 999999)}-{random.randint(100000, 999999)}"
            response = {"success": True, "api_key": key}
        elif "/api/data/report" in path:
            email = payload.get("email", "anonymous")
            bytes_shared = payload.get("bytes", 0)
            device_id = payload.get("device_id", "unknown")
            print(f"[BW FEED] {email} on {device_id} shared {bytes_shared} bytes.")
            response = {
                "success": True,
                "earned_credits": round(bytes_shared / (1024*1024*1024) * 0.10, 4),
                "status": "FEEDING_ACTIVE"
            }
        else:
            response = {"status": "SUCCESS"}

        self.wfile.write(json.dumps(response).encode('utf-8'))
