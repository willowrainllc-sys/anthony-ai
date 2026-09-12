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
            domain_query = query_params.get("domain", ["example.com"])[0].lower()
            # Wholesale pricing logic (NameSilo wholesale + 40% margin)
            wholesale_price = 10.50
            retail_price = 14.70 if domain_query.endswith(".com") else 19.99
            payload = {
                "domain": domain_query,
                "available": True,
                "price": retail_price,
                "wholesale_cost": wholesale_price,
                "registrar": "NameSilo Wholesale API v1",
                "status": "INGRESS_READY"
            }
        elif "/news/brief" in path:
            payload = {
                "status": "success",
                "headline": "DAILY INTEL: Obsidian City Marketplace Live",
                "brief": "Industrial-grade consumer ecosystem active. Deploy your identity on the global grid instantly.",
                "persona": "Obsidian City Director"
            }
        elif "/dashboard" in path:
            payload = [
                {
                    "title": "🔥 TODAY'S TRENDING INVESTIGATIONS",
                    "videos": [
                        {
                            "title": "The Awakening: Initial Discovery in Sci-Fi",
                            "views": "142K views",
                            "posted": "Just Now",
                            "thumbnail": "https://images.unsplash.com/photo-1506318137071-a8e063b4b4bf?q=80&w=600",
                            "video_url": "https://youtube.com/shorts/KdgJYtiCvLQ"
                        },
                        {
                            "title": "A Military Pilot Locked Radar onto a Metallic Sphere Moving at Mach 4",
                            "views": "289K views",
                            "posted": "10m ago",
                            "thumbnail": "https://images.unsplash.com/photo-1545143333-14387679366a?q=80&w=600",
                            "video_url": "https://youtube.com/shorts/Ii2TM2-Q1f0"
                        }
                    ]
                }
            ]
        else:
            payload = {
                "temporal": {"status": "QUANTUM_LOCK", "drift": 0.0012},
                "queue": {"pending_tasks": 0, "active_jobs": 1},
                "last_burst": {"node": "YOUTUBE", "time": now - 120},
                "missions": [
                    {"title": "QUANTUM GRID SYNCHRONIZED", "channel": "YOUTUBE", "priority": 90}
                ],
                "crypto_bets": [
                    {"asset": "BTC/USD", "amount": round(64250.00 + random.uniform(-150, 250), 2), "timestamp": now},
                    {"asset": "ETH/USD", "amount": round(3480.00 + random.uniform(-20, 30), 2), "timestamp": now}
                ],
                "timestamp": now
            }

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
            email = payload.get("email", "director@obsidian.city")
            session_id = f"sess_{int(time.time())}_{random.randint(1000,9999)}"
            response = {"success": True, "session_id": session_id, "email": email, "message": "Session authorized and saved."}
        elif "/api/domains/register" in path:
            response = {"success": True, "message": f"Identity [{payload.get('domain')}] secured via NameSilo wholesale gateway."}
        elif "/api/settle/authorize" in path:
            response = {"success": True, "status": "AUTHORIZED_PULSE", "txid": "TX-VERCEL-EDGE"}
        else:
            response = {"status": "SUCCESS", "message": "Pulse received."}

        self.wfile.write(json.dumps(response).encode('utf-8'))
