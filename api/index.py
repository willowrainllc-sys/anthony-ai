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

        if "/api/domains/search" in path:
            q = query_params.get("domain", ["mybrand"])[0].lower().split('.')[0]

            # 🔱 WHOLESALE LIBRARY GENERATOR (REDO WITH ADVANCED FEATURES)
            tlds = [
                {"tld": ".com", "price": 14.70, "tag": "Recommended", "status": "Taken"},
                {"tld": ".rocks", "price": 7.99, "tag": "Recommended", "status": "Available"},
                {"tld": ".city", "price": 9.99, "tag": "Exclusive", "status": "Available"},
                {"tld": ".ai", "price": 59.99, "tag": "Trending", "status": "Available"},
                {"tld": ".io", "price": 19.99, "tag": "Tech", "status": "Available"},
                {"tld": ".net", "price": 16.99, "tag": "Classic", "status": "Available"},
                {"tld": ".org", "price": 12.99, "tag": "Trust", "status": "Available"}
            ]

            results = []
            for item in tlds:
                results.append({
                    "domain": f"{q}{item['tld']}",
                    "available": item['status'] == "Available",
                    "price": item['price'],
                    "tag": item['tag'],
                    "registrar": "NameSilo Wholesale API v1"
                })

            payload = {
                "query": q,
                "results": results,
                "status": "INGRESS_READY",
                "timestamp": now
            }
        elif "/api/auth/session" in path:
            payload = {"session": "active", "timestamp": now}
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
            session_id = f"sess_{int(time.time())}_{random.randint(1000,9999)}"
            response = {"success": True, "session_id": session_id, "email": email}
        elif "/api/settle/authorize" in path:
            response = {"success": True, "status": "AUTHORIZED", "txid": f"TX-{int(time.time())}"}
        else:
            response = {"status": "SUCCESS"}

        self.wfile.write(json.dumps(response).encode('utf-8'))
