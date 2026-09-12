# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- VERCEL SERVERLESS API GATEWAY FOR OBSIDIAN CITY ---
import time
import json
import random
import os
import urllib.parse
from http.server import BaseHTTPRequestHandler

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

        # 🔱 LOGGING INGRESS
        print(f"[INGRESS] GET {path} | Query: {query_params}")

        if "/api/domains/search" in path or "/search" in path:
            q = query_params.get("domain", query_params.get("q", ["mybrand"]))[0].lower().split('.')[0]

            # 🔱 WHOLESALE LIBRARY GENERATOR (ULTIMATE PROFIT MODEL)
            tlds = [
                {"tld": ".com", "cost": 10.50, "retail": 14.70, "tag": "Best Value"},
                {"tld": ".ai", "cost": 45.00, "retail": 59.99, "tag": "Trending"},
                {"tld": ".io", "cost": 15.00, "retail": 19.99, "tag": "Tech"},
                {"tld": ".city", "cost": 6.50, "retail": 9.99, "tag": "Exclusive"},
                {"tld": ".rocks", "cost": 5.00, "retail": 7.99, "tag": "Recommended"},
                {"tld": ".net", "cost": 12.00, "retail": 16.99, "tag": "Classic"},
                {"tld": ".org", "cost": 9.50, "retail": 12.99, "tag": "Trust"}
            ]

            results = []
            for item in tlds:
                results.append({
                    "domain": f"{q}{item['tld']}",
                    "available": True,
                    "price": item['retail'],
                    "wholesale_cost": item['cost'],
                    "tag": item['tag'],
                    "registrar": "Obsidian Wholesale Pool v1"
                })

            payload = {
                "query": q,
                "results": results,
                "status": "INGRESS_READY",
                "timestamp": now
            }
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

        print(f"[INGRESS] POST {path} | Payload: {payload}")

        if "/api/auth/signin" in path:
            email = payload.get("email", "user@example.com")
            sid = f"sess_{int(time.time())}_{random.randint(1000,9999)}"
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
