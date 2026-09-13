# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY SOVEREIGN HOSTING SERVER v1.1 ---
import http.server
import socketserver
import os
import sys
import urllib.parse
import json

# 🔱 Import your existing Vercel API logic
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
try:
    from index import handler
except ImportError:
    class handler:
        def do_GET(self): pass
        def do_POST(self): pass

PORT = 8080
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class SovereignHandler(http.server.SimpleHTTPRequestHandler):
    """
    Extends standard server to handle clean URLs and proxy to Vercel logic.
    """
    def do_GET(self):
        # 1. Route API calls to your index.py logic
        if self.path.startswith('/api/'):
            # Create a mock instance of your handler
            from index import handler as APIHandler
            api_instance = APIHandler(self.request, self.client_address, self.server)
            return

        # 2. Clean URL Routing (Mirroring vercel.json for local environment)
        routing = {
            "/dashboard": "obsidian_city_dashboard.html",
            "/domains": "obsidian_domains.html",
            "/search": "obsidian_domain_results.html",
            "/checkout": "obsidian_unified_checkout.html",
            "/vps": "obsidian_vps_hosting.html",
            "/leo": "obsidian_leo_builder.html",
            "/signin": "obsidian_signin.html",
            "/register": "obsidian_register.html",
            "/profile": "obsidian_user_profile.html",
            "/help": "obsidian_help_center.html",
            "/llc": "obsidian_llc_formation.html"
        }

        # Strip query params for routing check
        clean_path = self.path.split('?')[0].rstrip('/')

        if clean_path in routing:
            self.path = "/" + routing[clean_path]
        elif clean_path == "" or clean_path == "/":
            self.path = "/index.html"

        # 3. Serve Static Files
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api/'):
            from index import handler as APIHandler
            api_instance = APIHandler(self.request, self.client_address, self.server)
            return
        self.send_error(405, "Method not allowed")

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    # Enable reuse of address to avoid "Address already in use" errors on restart
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SovereignHandler) as httpd:
        print(f"\n" + "="*50)
        print(f"🔱 OBSIDIAN CITY SOVEREIGN HOSTING ACTIVE")
        print(f"[*] URL: http://localhost:{PORT}")
        print(f"[*] Update Mode: UNLIMITED (Direct File Serving)")
        print("="*50 + "\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Server Deactivated.")
            sys.exit(0)
