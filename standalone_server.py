# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY SOVEREIGN HOSTING SERVER v1.3 ---
import http.server
import socketserver
import os
import sys
import urllib.parse
import json
import asyncio

# 🔱 Import decoupled logic from api/index.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
try:
    from index import handle_api_get, handle_api_post
except ImportError:
    handle_api_get = None
    handle_api_post = None

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class SovereignHandler(http.server.SimpleHTTPRequestHandler):
    """
    Standard server with direct bridge to decoupled API logic.
    """
    def do_GET(self):
        if self.path.startswith('/api/') and handle_api_get:
            parsed_path = urllib.parse.urlparse(self.path)
            query_params = urllib.parse.parse_qs(parsed_path.query)

            # Execute logic
            result = asyncio.run(handle_api_get(parsed_path.path, query_params))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            return

        # Clean URL Routing
        routing = {
            "/dashboard": "obsidian_city_dashboard.html",
            "/domains": "obsidian_domains.html",
            "/search": "obsidian_domain_results.html",
            "/checkout": "obsidian_unified_checkout.html",
            "/vps": "obsidian_vps_hosting.html",
            "/builder": "obsidian_ai_builder.html",
            "/signin": "obsidian_signin.html",
            "/register": "obsidian_register.html",
            "/help": "obsidian_help_center.html",
            "/llc": "obsidian_llc_formation.html"
        }

        clean_path = self.path.split('?')[0].rstrip('/')
        if clean_path in routing:
            self.path = "/" + routing[clean_path]
        elif clean_path == "" or clean_path == "/":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/') and handle_api_post:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            payload = json.loads(post_data) if post_data else {}

            # Execute logic
            result = asyncio.run(handle_api_post(self.path, payload, self.client_address[0]))

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode('utf-8'))
            return

        self.send_error(405, "Method not allowed")

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

if __name__ == "__main__":
    os.chdir(DIRECTORY)

    # [+] ARES SELF-HEALING BOOTSTRAP
    print(f"[+] ARES CORE: Initiating Self-Healing Protocol...")
    try:
        import subprocess
        subprocess.Popen([sys.executable, "colony_backend/ares_master_empire_fixer.py"])
    except: pass

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SovereignHandler) as httpd:
        print(f"\n" + "="*50)
        print(f"[+] OBSIDIAN CITY STANDALONE SERVER v1.3 ACTIVE")
        print(f"[*] URL: http://localhost:{PORT}")
        print("="*50 + "\n")
        httpd.serve_forever()
