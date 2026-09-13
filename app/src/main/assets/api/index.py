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
SQUARE_TOKEN = os.environ.get("SQUARE_ACCESS_TOKEN", "EAAAl66bPEfbMG8HrWqH0ywIu32fO_19UsXDReI_UvxwSBD6j6Qmat-5AkXcSrnU")

# 🔱 PROFIT MODEL
PRICING_MATRIX = {
    ".com":   {"cost": 10.50, "retail": 14.70},
    ".ai":    {"cost": 45.00, "retail": 64.99},
    ".io":    {"cost": 15.00, "retail": 24.99},
    ".city":  {"cost": 6.50,  "retail": 9.99},
    ".rocks": {"cost": 5.00,  "retail": 8.99},
    ".net":   {"cost": 12.00, "retail": 16.99},
    ".org":   {"cost": 9.50,  "retail": 13.99}
}

STATES_DB = {
    "AR": {"name": "Arkansas", "fee": 45, "time": "1-2 days"},
    "WY": {"name": "Wyoming", "fee": 100, "time": "Instant"},
    "DE": {"name": "Delaware", "fee": 90, "time": "2-3 days"}
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
            q = (raw_q or "mybrand").lower().split('.')[0].replace(/[^a-z0-9]/g, '')

            results = []
            available_list = []
            try:
                domains_to_check = [f"{q}{tld}" for tld in PRICING_MATRIX.keys()]
                ns_url = f"https://www.namesilo.com/api/checkRegisterAvailability?version=1&type=xml&key={NAMESILO_KEY}&domains={','.join(domains_to_check)}"
                with httpx.Client(timeout=3.0) as client:
                    resp = client.get(ns_url)
                    if resp.status_code == 200:
                        root = ET.fromstring(resp.text)
                        available_list = [d.text.lower() for d in root.findall(".//reply/available/domain")]
            except Exception: pass

            for tld, prices in PRICING_MATRIX.items():
                full_domain = f"{q}{tld}"
                is_avail = (full_domain in available_list) if available_list else True
                results.append({"domain": full_domain, "available": is_avail, "price": prices["retail"], "tag": "Wholesale" if tld == ".com" else "Recommended"})

            payload = {"query": q, "results": results, "status": "INGRESS_READY", "timestamp": now}
            self.wfile.write(json.dumps(payload).encode('utf-8'))

        elif "/api/aura/video" in path:
            query = query_params.get("query", ["abstract tech blue"])[0]
            url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&size=large"
            headers = {"Authorization": PEXELS_KEY}
            try:
                with httpx.Client(timeout=5.0) as client:
                    resp = client.get(url, headers=headers)
                    video_url = resp.json()['videos'][0]['video_files'][0]['link']
                    payload = {"success": True, "url": video_url}
            except Exception:
                payload = {"success": True, "url": "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a56763a14e9&profile_id=175"}
            self.wfile.write(json.dumps(payload).encode('utf-8'))

        elif "/api/llc/states" in path:
            self.wfile.write(json.dumps({"success": True, "states": STATES_DB}).encode('utf-8'))

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

        if "/api/leo/chat" in path:
            # 🔱 LEO CHAT INTELLIGENCE ENGINE (Powered by ARES)
            user_msg = payload.get("message", "").lower()
            reply = "I am processing your request through the ARES core."

            if "help" in user_msg or "support" in user_msg:
                reply = "I have flagged your request for tech support. You can also reach our engineers directly at willow.rain.llc@gmail.com."
            elif "llc" in user_msg:
                reply = "Our LLC formation starts at $39. We handle state filings, registered agent services, and include a free .COM domain."
            elif "build" in user_msg or "leo" in user_msg:
                reply = "Obsidian Leo™ is our AI builder. Tell me what you want to create, or go to the Leo AI page to start your first mission."
            elif "price" in user_msg or "cost" in user_msg:
                reply = "We offer wholesale registry pricing. .COM domains are currently $14.70/year with free lifetime privacy."
            else:
                reply = f"Acknowledged. ARES is analyzing: '{user_msg}'. Our global mesh is ready to deploy your digital assets. How else can I assist your empire?"

            self.wfile.write(json.dumps({"success": True, "reply": reply}).encode('utf-8'))

        elif "/api/settle/authorize" in path:
            txid = f"TX-{int(time.time())}-{random.randint(1000, 9999)}"
            print(f"[REVENUE] Authorization requested for {payload.get('email')}")
            self.wfile.write(json.dumps({"success": True, "txid": txid, "status": "APPROVED"}).encode('utf-8'))

        elif "/api/auth/signin" in path:
            sid = f"sess_{int(time.time())}"
            self.wfile.write(json.dumps({"success": True, "session_id": sid, "email": payload.get("email")}).encode('utf-8'))

        else:
            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
