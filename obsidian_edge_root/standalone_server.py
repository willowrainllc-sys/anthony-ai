# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY SOVEREIGN HOSTING SERVER v1.0 ---
import http.server
import socketserver
import os
import sys

# 🔱 Import your existing Vercel API logic
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))
from index import handler

PORT = 8080  # Changed to 8080 for easier local testing without admin rights
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class SovereignHandler(handler):
    """
    Extends your existing Vercel logic to handle static files
    AND API calls on your own hardware.
    """
    def do_GET(self):
        # 1. Route API calls to your existing logic
        if self.path.startswith('/api/'):
            return super().do_GET()

        # 2. Clean URL Routing (Mirroring vercel.json)
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
            "/help": "obsidian_help_center.html"
        }

        target = routing.get(self.path.split('?')[0])
        if target:
            self.path = "/" + target

        # 3. Serve Static Files
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path.startswith('/api/'):
            return super().do_POST()
        self.send_error(405, "Method not allowed")

if __name__ == "__main__":
    os.chdir(DIRECTORY)
    with socketserver.TCPServer(("", PORT), SovereignHandler) as httpd:
        print(f"🔱 OBSIDIAN CITY SOVEREIGN HOSTING ACTIVE")
        print(f"[*] Port: {PORT}")
        print(f"[*] Update Mode: UNLIMITED")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[-] Server Deactivated.")
            sys.exit(0)
