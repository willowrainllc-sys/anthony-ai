# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY SOVEREIGN HOSTING SERVER v1.2 ---
import http.server
import socketserver
import os
import sys
import urllib.parse
import json

# 🔱 Import your existing Vercel API logic
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
try:
    from index import handler as APIHandler
except ImportError:
    APIHandler = None

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class SovereignHandler(http.server.SimpleHTTPRequestHandler):
    """
    Extends standard server to handle clean URLs and proxy to Vercel logic.
    """
    def do_GET(self):
        # 1. Route API calls to your index.py logic
        if self.path.startswith('/api/') and APIHandler:
             # Manually trigger the API handler do_GET without re-parsing the socket
             api_instance = APIHandler.__new__(APIHandler)
             api_instance.request = self.request
             api_instance.client_address = self.client_address
             api_instance.server = self.server
             api_instance.rfile = self.rfile
             api_instance.wfile = self.wfile
             api_instance.headers = self.headers
             api_instance.path = self.path
             api_instance.command = self.command
             api_instance.close_connection = True # Ensure connection closes after API call

             try:
                 api_instance.do_GET()
             except Exception as e:
                 print(f"[-] API Bridge Error: {e}")
                 self.send_error(500, f"API Error: {e}")
             return

        # 2. Clean URL Routing
        routing = {
            "/dashboard": "obsidian_city_dashboard.html",
            "/domains": "obsidian_domains.html",
            "/search": "obsidian_domain_results.html",
            "/checkout": "obsidian_unified_checkout.html",
            "/vps": "obsidian_vps_hosting.html",
            "/obsidian-ai": "obsidian_ai_builder.html",
            "/builder": "obsidian_ai_builder.html",
            "/signin": "obsidian_signin.html",
            "/register": "obsidian_register.html",
            "/profile": "obsidian_user_profile.html",
            "/help": "obsidian_help_center.html",
            "/llc": "obsidian_llc_formation.html",
            "/llc-intake": "obsidian_llc_intake.html",
            "/start-llc": "obsidian_llc_state.html"
        }

        clean_path = self.path.split('?')[0].rstrip('/')

        # 🔱 pSEO Dynamic Route Handling (Mocking /start-llc/)
        if clean_path.startswith("/start-llc/"):
            state_code = clean_path.split("/")[-1].upper()
            self.path = f"/obsidian_llc_state.html?state={state_code}"
            return super().do_GET()

        if clean_path in routing:
            self.path = "/" + routing[clean_path]
        elif clean_path == "" or clean_path == "/":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/') and APIHandler:
             api_instance = APIHandler.__new__(APIHandler)
             api_instance.request = self.request
             api_instance.client_address = self.client_address
             api_instance.server = self.server
             api_instance.rfile = self.rfile
             api_instance.wfile = self.wfile
             api_instance.headers = self.headers
             api_instance.path = self.path
             api_instance.command = self.command
             api_instance.close_connection = True

             try:
                 api_instance.do_POST()
             except Exception as e:
                 print(f"[-] API Bridge Error (POST): {e}")
                 self.send_error(500, f"API Error: {e}")
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

    # 🔱 HARD-CODED ARES AUTO-IGNITE
    print(f"🔱 ARES CORE: Initiating Hard-Coded Self-Healing Protocol...")
    try:
        import subprocess
        # Run Master Fixer in a separate process to avoid blocking
        subprocess.Popen([sys.executable, "colony_backend/ares_master_empire_fixer.py"])
        print(f"✓ ARES CORE: Self-healing background mission dispatched.")
    except Exception as e:
        print(f"[-] ARES CORE: Auto-ignite notice: {e}")

    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SovereignHandler) as httpd:
        print(f"\n" + "="*50)
        print(f"🔱 OBSIDIAN CITY SOVEREIGN HOSTING v1.2 ACTIVE")
        print(f"[*] URL: http://localhost:{PORT}")
        print(f"[*] API Bridge: NameSilo + Pexels 4K Active")
        print("="*50 + "\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Server Deactivated.")
            sys.exit(0)
