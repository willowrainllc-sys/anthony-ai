# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- VERCEL SERVERLESS API GATEWAY FOR OBSIDIAN CITY ---
import time
import json
import random
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler

# 🔱 PROFIT MODEL: Wholesale (Registry Cost) vs Retail (Our Price)
WHOLESALE_COSTS = {
    ".com": 10.50,
    ".rocks": 4.99,
    ".city": 6.50,
    ".ai": 45.00,
    ".io": 15.00,
    ".net": 12.00,
    ".org": 9.50
}

RETAIL_PRICES = {
    ".com": 14.70,
    ".rocks": 7.99,
    ".city": 9.99,
    ".ai": 59.99,
    ".io": 19.99,
    ".net": 16.99,
    ".org": 12.99
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
            q = query_params.get("domain", ["mybrand"])[0].lower().split('.')[0].replace(/[^a-z0-9]/g, '')

            results = []
            for tld, retail in RETAIL_PRICES.items():
                cost = WHOLESALE_COSTS[tld]
                results.append({
                    "domain": f"{q}{tld}",
                    "available": True,
                    "price": retail,
                    "wholesale_cost": cost,
                    "margin": round(retail - cost, 2),
                    "tag": "Wholesale Cost" if retail == min(RETAIL_PRICES.values()) else "Recommended",
                    "registrar": "Obsidian Wholesale Pool v1"
                })

            payload = {
                "query": q,
                "results": results,
                "status": "INGRESS_READY",
                "timestamp": now
            }
        elif "/api/auth/session" in path:
            sid = query_params.get("sid", [None])[0]
            payload = {"active": sid in SESSIONS, "user": SESSIONS.get(sid)}
        else:
            payload = {"status": "SUCCESS", "timestamp": now}

        self.wfile.write(json.dumps(payload).encode('utf-8'))

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
            SESSIONS[sid] = {"email": email, "last_active": time.time()}
            response = {"success": True, "session_id": sid, "email": email}
        elif "/api/settle/authorize" in path:
            response = {
                "success": True,
                "status": "AUTHORIZED",
                "txid": f"TX-{int(time.time())}",
                "provisioning": "QUEUED"
            }
        else:
            response = {"status": "SUCCESS"}

        self.wfile.write(json.dumps(response).encode('utf-8'))
