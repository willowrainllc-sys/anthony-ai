# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v6.0 (SOVEREIGN NATIVE WEB) ---
import os
import sys
import json
import time
import mimetypes
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from swarm_logger import swarm_log
from swarm_persistence import db
from obsidian_domain_registry import domain_registry

# Paths
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
PORTAL_DIR = ROOT / "willow_rain_global" / "wholesale_portal"
UI_DIR = ROOT / "saturn_cloud" / "dashboard_ui"
APK_DIR = ROOT / "app" / "build" / "outputs" / "apk" / "debug"
VIDEO_DIR = ROOT / "secure_assets" / "source_videos"

PORT = 80

class SovereignWebHandler(BaseHTTPRequestHandler):
    """
    SOVEREIGN NATIVE WEB HANDLER:
    1. INDEPENDENT: No FastAPI, No external frameworks.
    2. SECURE: Maestas Root Key authentication.
    3. NATIVE: Direct SQLite and File System ingress.
    """
    def do_GET(self):
        url = urlparse(self.path)

        # 1. API Endpoints
        if url.path == "/api/feed":
            self._handle_api_feed()
            return

        if url.path == "/api/revenue/vitals":
            self._handle_api_vitals()
            return

        if url.path == "/download/titan_windows.zip":
            self._serve_file(PORTAL_DIR / "downloads" / "titan_browser_win_x64.zip", as_attachment=True, filename="titan_browser_win.zip")
            return

        if url.path == "/download/obsidian_ai_studio.zip":
            self._serve_file(PORTAL_DIR / "obsidian_ai_studio_v1.zip", as_attachment=True, filename="obsidian_ai_studio.zip")
            return

        if url.path == "/download/obsidian.apk":
            self._handle_apk_download()
            return

        # 2. Domain Mapping
        host = self.headers.get("Host", "obsidian-global.io").split(":")[0]
        domain_map = domain_registry.get_domain_map()
        target_file = domain_map.get(host, "obsidian_world_gateway.html")

        # 🔱 PUBLIC ACCESS BYPASS: Industrial Landing Pages
        public_domains = ["titan-browser.io", "www.mywebbrowser.com", "vortex-global.io", "ghost-vault.com", "brick-bitcoin.net", "sovereign-node.org", "black-hole.media", "global-pay.io", "obsidian-registry.io", "gov-strike.io", "obsidian-store.io", "obsidian-hosting.io", "obsidian-striker.io", "obsidian.city", "www.obsidian.city", "ide.obsidian-global.io", "wiki.obsidian-global.io", "b2b.obsidian-global.io", "town360.com", "www.town360.com", "io-factory.obsidian-global.io"]

        # 🔱 MASTER BRIDGE RESOLVER
        # If accessing via the Global Bridge (trycloudflare), default to the OMNI_GRID Command
        is_bridge = "trycloudflare.com" in host
        if is_bridge and (target_file == "obsidian_world_gateway.html" or target_file == "obsidian_master_hub.html"):
            target_file = "omni_grid_command.html"

        # If accessing a landing page or public domain, serve without auth
        if host in public_domains or is_bridge or target_file.endswith("_landing.html") or "marketplace" in target_file or target_file == "omni_grid_command.html" or target_file == "enterprise_storefront_hub.html":
            swarm_log(f"🌐 PUBLIC INGRESS: Serving [{host}] -> {target_file}", node="SUPREME")
            # Fallback to voyager_landing if specific landing doesn't exist yet
            final_path = PORTAL_DIR / target_file
            if not final_path.exists():
                final_path = PORTAL_DIR / "titan_landing.html"
            self._serve_file(final_path)
            return

        # 3. Sovereign Gateway (Open Ingress for Obsidian City)
        # Authentication layer removed as requested by Director
        if "obsidian-global.io" in host:
            target_file = "obsidian_os_desktop.html"

        # UI Overrides
        if url.path.startswith("/ui/"):
            file_path = UI_DIR / url.path.replace("/ui/", "")
        else:
            file_path = PORTAL_DIR / target_file
            if not file_path.exists():
                file_path = UI_DIR / target_file

        self._serve_file(file_path)

    def _handle_api_feed(self):
        """Native JSON feed from SQLite database."""
        try:
            with db._get_connection() as conn:
                rows = conn.execute("SELECT id, title, description, video_url, thumbnail_url FROM ai_videos ORDER BY created_at DESC LIMIT 20").fetchall()

            videos = []
            for r in rows:
                videos.append({
                    "id": r[0],
                    "title": r[1],
                    "description": r[2],
                    "video_url": r[3],
                    "thumbnail_url": r[4]
                })

            # Fallback if DB empty
            if not videos:
                videos = [
                    {"id": "v1", "title": "SOVEREIGN NEURAL LINK", "description": "100% Native Grid.", "video_url": "https://example.com/v1.mp4", "thumbnail_url": ""}
                ]

            self._send_json(videos)
        except Exception as e:
            self._send_error(500, str(e))

    def _handle_apk_download(self):
        # Industrial Strength Path Resolution
        apk_path = (ROOT / "app" / "build" / "outputs" / "apk" / "debug" / "app-debug.apk").resolve()

        if apk_path.exists() and apk_path.is_file():
            swarm_log(f"🌐 WEB: Dispatching APK Strike -> [{apk_path}]", node="SUPREME")
            self._serve_file(apk_path, as_attachment=True, filename="obsidian_global_v26.apk")
        else:
            swarm_log(f"[-] WEB ERROR: APK not found at {apk_path}", node="SUPREME")
            self._send_error(404, "Build in progress or file moved. Verify path in Sovereign IDE.")

    def _serve_file(self, file_path: Path, as_attachment=False, filename=None):
        if not file_path.exists() or not file_path.is_file():
            self._send_error(404, "Resource Not Found")
            return

        self.send_response(200)
        content_type, _ = mimetypes.guess_type(str(file_path))
        self.send_header('Content-Type', content_type or 'application/octet-stream')

        if as_attachment:
            self.send_header('Content-Disposition', f'attachment; filename="{filename or file_path.name}"')

        stat = file_path.stat()
        self.send_header('Content-Length', stat.st_size)
        self.end_headers()

        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())

    def _send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def _send_error(self, code, message):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(message.encode('utf-8'))

    def _get_cookie(self, name):
        cookies = self.headers.get('Cookie', '')
        for c in cookies.split(';'):
            if '=' in c:
                k, v = c.strip().split('=', 1)
                if k == name: return v
        return None

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, SovereignWebHandler)
    swarm_log(f"🔱 WEB_SERVER: Sovereign Native Hosting ONLINE on Port {PORT}.", node="SUPREME")
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
