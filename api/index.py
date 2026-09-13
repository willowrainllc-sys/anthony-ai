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

# 🔱 WHOLESALE CREDENTIALS
NAMESILO_KEY = os.environ.get("NAMESILO_API_KEY", "cert_O6RAXSvTTLkhX1TlQcQt9wpA")
# ResellerClub V2 Authentication
RC_API_KEY = os.environ.get("RESELLERCLUB_KEY", "mock_key")
RC_USER_ID = os.environ.get("RESELLERCLUB_ID", "123456")

# 🔱 PROFIT MODEL: Wholesale Cost vs Retail Price
# We set retail prices to capture a healthy margin for the Boss.
PRICING_MATRIX = {
    ".com":   {"cost": 10.50, "retail": 14.70},
    ".ai":    {"cost": 45.00, "retail": 59.99},
    ".io":    {"cost": 15.00, "retail": 19.99},
    ".city":  {"cost": 6.50,  "retail": 9.99},
    ".rocks": {"cost": 5.00,  "retail": 7.99},
    ".net":   {"cost": 12.00, "retail": 16.99},
    ".org":   {"cost": 9.50,  "retail": 12.99}
}

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

            # 🔱 1. Attempt NameSilo Wholesale Handshake
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

            # 🔱 2. Attempt ResellerClub Failover (using V2 Headers)
            if not available_list and RC_API_KEY != "mock_key":
                try:
                    rc_url = "https://api.resellerclub.com/v2/domains/availability"
                    headers = {
                        "Authorization": f"ApiKey {RC_API_KEY}",
                        "X-User-Id": RC_USER_ID
                    }
                    params = {"domainNames": q, "tlds": list(PRICING_MATRIX.keys())}
                    with httpx.Client(timeout=3.0) as client:
                        resp = client.get(rc_url, headers=headers, params=params)
                        if resp.status_code == 200:
                            # RC V2 logic: { "domain": "status", ... }
                            data = resp.json()
                            available_list = [d for d, s in data.items() if s == "available"]
                            source = "ResellerClub V2 Hub"
                except Exception: pass

            # 🔱 3. Build Profit-Margin Results
            for tld, prices in PRICING_MATRIX.items():
                full_domain = f"{q}{tld}"
                is_avail = (full_domain in available_list) if available_list else True
                results.append({
                    "domain": full_domain,
                    "available": is_avail,
                    "price": prices["retail"],
                    "cost": prices["cost"],
                    "profit": round(prices["retail"] - prices["cost"], 2),
                    "tag": "Wholesale" if tld == ".com" else "Recommended",
                    "distributor": source
                })

            payload = {"query": q, "results": results, "status": "INGRESS_READY", "timestamp": now}
            self.wfile.write(json.dumps(payload).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({"status": "SUCCESS"}).encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"success": True, "txid": f"TX-{int(time.time())}"}).encode('utf-8'))
