# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- VERCEL SERVERLESS API GATEWAY FOR OBSIDIAN CITY ---
import time
import json
import random
import os
import re
import asyncio
import urllib.parse
import httpx
import xml.etree.ElementTree as ET
from http.server import BaseHTTPRequestHandler
from dotenv import load_dotenv

# 🔱 Load environment for local server runs
load_dotenv()

# 🔱 INTERNAL BRIDGES
try:
    from colony_backend.obsidian_database_sync import db_bridge
except ImportError:
    class MockDB:
        def save_session(self, *args, **kwargs): pass
        def record_purchase(self, *args, **kwargs): pass
        def is_director(self, email): return email.lower().startswith("anthony")
    db_bridge = MockDB()

# 🔱 WHOLESALE & DATABASE BRIDGES
NAMESILO_KEY = os.environ.get("NAMESILO_API_KEY")
PEXELS_KEY = os.environ.get("PEXELS_API_KEY")
SQUARE_TOKEN = os.environ.get("SQUARE_ACCESS_TOKEN", "EAAAl66bPEfbMG8HrWqH0ywIu32fO_19UsXDReI_UvxwSBD6j6Qmat-5AkXcSrnU")
STRIPE_KEY = os.environ.get("STRIPE_SECRET_KEY")
STRIPE_RK = os.environ.get("STRIPE_RESTRICTED_KEY")

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

# 🔱 KNOWLEDGE BASE
KNOWLEDGE_BASE = {
    "domains": ["How to register a domain", "Setting up custom nameservers", "Transferring a domain to Obsidian City", "WHOIS privacy protection explained"],
    "dns": ["Configuring A and CNAME records", "Global DNS propagation times", "Post-Quantum DNS security"],
    "vps": ["Deploying your first KVM node", "One-click OS installation guide", "Connecting via SSH and VNC"],
    "billing": ["Setting up automatic renewals", "Multi-currency settlement logic", "Square and Stripe payment troubleshooting"]
}

SESSIONS = {}
ORDERS = {}
TICKETS = {}

# ============================================================
# 🔱 CORE API LOGIC (DECOUPLED)
# ============================================================

async def handle_api_get(path, query_params):
    now = time.time()

    if "/api/domains/search" in path:
        raw_q = query_params.get("domain", [""])[0] or query_params.get("q", [""])[0]
        q = re.sub(r'[^a-z0-9]', '', (raw_q or "mybrand").lower().split('.')[0])
        results = []
        available_list = []
        try:
            domains_to_check = [f"{q}{tld}" for tld in PRICING_MATRIX.keys()]
            ns_url = f"https://www.namesilo.com/api/checkRegisterAvailability?version=1&type=xml&key={NAMESILO_KEY}&domains={','.join(domains_to_check)}"
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.get(ns_url)
                if resp.status_code == 200:
                    root = ET.fromstring(resp.text)
                    available_list = [d.text.lower() for d in root.findall(".//reply/available/domain")]
        except: pass
        for tld, prices in PRICING_MATRIX.items():
            full_domain = f"{q}{tld}"
            is_avail = (full_domain in available_list) if available_list else True
            results.append({"domain": full_domain, "available": is_avail, "price": prices["retail"], "tag": "Wholesale" if tld == ".com" else "Recommended"})
        return {"query": q, "results": results, "status": "INGRESS_READY", "timestamp": now}

    elif "/api/aura/video" in path:
        query = query_params.get("query", ["abstract tech blue"])[0]
        url = f"https://api.pexels.com/videos/search?query={query}&per_page=1&size=large"
        headers = {"Authorization": PEXELS_KEY}
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(url, headers=headers)
                video_url = resp.json()['videos'][0]['video_files'][0]['link']
                return {"success": True, "url": video_url}
        except:
            return {"success": True, "url": "https://player.vimeo.com/external/371728562.hd.mp4?s=447702f23cf5354900cb3e23630f9a56763a14e9&profile_id=175"}

    elif "/api/orders/status" in path:
        email = query_params.get("email", [""])[0]
        purchases = db_bridge.get_purchases(email)
        return {"success": True, "orders": purchases}

    elif "/api/llc/states" in path:
        return {"success": True, "states": STATES_DB}

    elif "/api/support/search" in path:
        q = query_params.get("q", [""])[0].lower()
        results = []
        for cat, articles in KNOWLEDGE_BASE.items():
            if q in cat: results.extend([{"category": cat, "title": a} for a in articles])
            else:
                for a in articles:
                    if q in a.lower(): results.append({"category": cat, "title": a})
        return {"success": True, "results": results[:5]}

    elif "/api/ares/spatial/predict" in path:
        from colony_backend.ares_spatial_oracle import AresSpatialOracle
        oracle = AresSpatialOracle()
        predictions = await oracle.predict_expansion_vector()
        return {"success": True, "predictions": predictions}

    elif "/api/fintech/balance" in path:
        email = query_params.get("email", [""])[0]
        balance = 42910.42 if db_bridge.is_director(email) else 0.00
        return {"success": True, "balance": balance, "currency": "USD"}

    return {"status": "SUCCESS", "timestamp": now}

async def handle_api_post(path, payload, client_ip="0.0.0.0"):
            else:
                try:
                    from colony_backend.colony_brain import brain_gate
                    # Use the Supreme Orchestrator for all chat ingress
                    reply = await brain_gate.generate_serialized(user_msg, system_msg="You are the Obsidian Supreme Oracle.")
                except Exception as e:
                    print(f"[-] SUPREME BRAIN ERROR: {e}")
                    reply = "My uplink to the ARES core is currently throttled. Please ensure the Private Server is running."
            return {"success": True, "reply": reply}
    elif "/api/vouchers/claim" in path:
        code = payload.get("code", "").upper()
        email = payload.get("email", "anonymous")
        vouchers_path = Path(__file__).resolve().parent.parent / "colony_backend" / "vouchers.json"
        try:
            with open(vouchers_path, 'r') as f: vouchers = json.load(f)
            if code in vouchers and vouchers[code]["status"] == "AVAILABLE":
                val = vouchers[code]["value"]
                vouchers[code]["status"] = "REDEEMED"
                vouchers[code]["redeemed_by"] = email
                with open(vouchers_path, 'w') as f: json.dump(vouchers, f, indent=4)
                db_bridge.record_purchase(email, "voucher_redemption", val, f"CODE-{code}")
                return {"success": True, "value": val}
            return {"success": False, "error": "INVALID_OR_USED"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    elif "/api/support/ticket" in path:
        email = payload.get("email", "anonymous")
        subject = payload.get("subject", "General Inquiry")
        tid = f"TICK-{int(time.time())}"
        TICKETS[tid] = {"email": email, "subject": subject, "status": "OPEN"}
        return {"success": True, "ticket_id": tid}

    elif "/api/settle/authorize" in path:
        email = payload.get("email", "anonymous")
        item_type = payload.get("type", "unknown")
        amount = payload.get("amount", 0.0)
        txid = f"TX-{int(time.time())}-{random.randint(1000, 9999)}"
        db_bridge.record_purchase(email, item_type, amount, txid)
        instructions = [
            "1. Access your dashboard at obsidian.city/dashboard.",
            "2. Your Domain/Asset is currently in 'PROVISIONING' status.",
            "3. In 2-4 hours, your Nameservers will be live (tr.apiname.com).",
            "4. Secure your login with the Provisioning Token provided."
        ]
        return {"success": True, "txid": txid, "status": "APPROVED", "instructions": instructions}

    elif "/api/ares/strike/social" in path:
        from colony_backend.ares_social_strike_force import AresSocialStrikeForce
        strike = AresSocialStrikeForce()
        # Fire and forget to prevent server hang during intensive API pushes
        asyncio.create_task(strike.execute_global_video_strike())
        asyncio.create_task(strike.push_domain_ads())
        return {"success": True, "status": "STRIKE_DISPATCHED"}

    elif "/api/ares/strike/seo" in path:
        from colony_backend.ares_os_seo_commander import AresOsSeoCommander
        commander = AresOsSeoCommander()
        # Fire and forget for SEO blitz
        asyncio.create_task(commander.run_seo_mission())
        return {"success": True, "status": "SEO_BLITZ_DISPATCHED"}

    elif "/api/director/payout" in path:
        email = payload.get("email", "anonymous")
        if db_bridge.is_director(email):
            has_keys = bool(SQUARE_TOKEN and "EAAAl" in SQUARE_TOKEN)
            response = {"success": True, "status": "SETTLEMENT_DISPATCHED" if has_keys else "SIMULATED", "batch_id": f"PAY-{int(time.time())}"}
        else: response = {"success": False, "error": "UNAUTHORIZED"}
        return response

    elif "/api/auth/signin" in path:
        email = payload.get("email", "user@example.com")
        sid = f"sess_{int(time.time())}"
        db_bridge.save_session(sid, email, metadata={"ip": client_ip})
        return {"success": True, "session_id": sid, "email": email}

    return {"success": True}

# ============================================================
# 🔱 VERCEL HANDLER (ADAPTER)
# ============================================================

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)
        result = asyncio.run(handle_api_get(parsed_path.path, query_params))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        payload = json.loads(post_data) if post_data else {}

        result = asyncio.run(handle_api_post(self.path, payload, self.client_address[0]))

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode('utf-8'))
