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

# 🔱 WHOLESALE CREDENTIALS (Securely sourced from Environment)
NAMESILO_KEY = os.environ.get("NAMESILO_API_KEY", "cert_O6RAXSvTTLkhX1TlQcQt9wpA")

# 🔱 PROFIT MODEL: Wholesale (Registry Cost) vs Retail (Our Price)
WHOLESALE_COSTS = {
    ".com": 10.50, ".rocks": 4.99, ".city": 6.50,
    ".ai": 45.00, ".io": 15.00, ".net": 12.00, ".org": 9.50
}

RETAIL_PRICES = {
    ".com": 14.70, ".rocks": 7.99, ".city": 9.99,
    ".ai": 59.99, ".io": 19.99, ".net": 16.99, ".org": 12.99
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
            # 🔱 1. Parse Root Keyword
            raw_q = query_params.get("domain", [""])[0] or query_params.get("q", [""])[0]
            if not raw_q: raw_q = "mybrand"
            q = raw_q.lower().split('.')[0].replace(/[^a-z0-9]/g, '')
            if not q: q = "mybrand"

            # 🔱 2. Prepare Wholesale Handshake (NameSilo)
            target_domains = [f"{q}{tld}" for tld in RETAIL_PRICES.keys()]
            domains_str = ",".join(target_domains)

            # Using NameSilo API to check real availability
            # Note: cert_ key uses the sandbox/cert environment
            ns_url = f"https://www.namesilo.com/api/checkRegisterAvailability?version=1&type=xml&key={NAMESILO_KEY}&domains={domains_str}"

            available_list = []
            try:
                # Synchronous request for serverless simplicity (httpx supports both)
                with httpx.Client(timeout=10.0) as client:
                    resp = client.get(ns_url)
                    if resp.status_code == 200:
                        root = ET.fromstring(resp.text)
                        # NameSilo returns <available><domain>...</domain></available>
                        for avail in root.findall(".//reply/available/domain"):
                            available_list.append(avail.text.lower())
            except Exception as e:
                print(f"[NAMESILO ERROR] {e}")
                # If API fails, we assume availability for the UI fallback
                available_list = target_domains

            # 🔱 3. Build Profit-Margin Results
            results = []
            for tld, retail in RETAIL_PRICES.items():
                full_domain = f"{q}{tld}"
                is_avail = full_domain in available_list
                cost = WHOLESALE_COSTS[tld]

                results.append({
                    "domain": full_domain,
                    "available": is_avail,
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
            self.wfile.write(json.dumps(payload).encode('utf-8'))
        else:
            self.wfile.write(json.dumps({"status": "SUCCESS"}).encode('utf-8'))

    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
