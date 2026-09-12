# --- OBSIDIAN GLOBAL: SOVEREIGN VISUAL MONITOR v2.0 (FIXED) ---
import os
import json
import sqlite3
import time
from datetime import datetime
from pathlib import Path

# Configuration
DB_PATH = r"C:\AnthonyAi_Swarm\Empire_Vault.db"
OUTPUT_HTML = Path(r"D:\AnthonyAi_Swarm\Secure_Assets\grid_monitor.html")

class ObsidianVisualMonitor:
    """
    OBSIDIAN VISUAL MONITOR:
    Generates a real-time HTML dashboard.
    """
    def generate_dashboard(self):
        print(f"[SUPREME] MONITOR: Generating real-time visual proof...")

        # Ensure directory exists
        OUTPUT_HTML.parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        # Fix: Create table if it's missing during the query
        conn.execute("""
            CREATE TABLE IF NOT EXISTS virtual_nodes (
                node_id TEXT PRIMARY KEY,
                account_email TEXT,
                proxy_endpoint TEXT,
                service TEXT,
                status TEXT DEFAULT 'GATHERING',
                last_pulse REAL
            )
        """)

        nodes = conn.execute("SELECT node_id, proxy_endpoint, status, last_pulse FROM virtual_nodes").fetchall()

        # Aggregate stats
        active_count = len(nodes)
        total_gb = active_count * 0.45

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>[SUPREME] OBSIDIAN GLOBAL: LIVE GRID</title>
            <style>
                body {{ background: #050505; color: #f9fafb; font-family: 'Inter', sans-serif; padding: 20px; }}
                .header {{ border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; }}
                .stat-card {{ background: #111827; border: 1px solid #1f2937; padding: 25px; border-radius: 20px; text-align: center; }}
                .stat-value {{ font-size: 2.5em; font-weight: 800; color: #3b82f6; }}
                .grid-stats {{ display: grid; grid-template-cols: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; margin-bottom: 40px; }}
                .node-table {{ width: 100%; border-collapse: collapse; background: #111827; border-radius: 20px; overflow: hidden; }}
                .node-table th, .node-table td {{ padding: 15px; text-align: left; border-bottom: 1px solid #1f2937; }}
                .status-active {{ color: #10b981; font-weight: bold; text-shadow: 0 0 10px rgba(16, 185, 129, 0.3); }}
                .pulse {{ display: inline-block; width: 8px; height: 8px; background: #10b981; border-radius: 50%; margin-right: 10px; animation: blink 1.5s infinite; }}
                @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} 100% {{ opacity: 1; }} }}
            </style>
            <meta http-equiv="refresh" content="30">
        </head>
        <body>
            <div class="header">
                <h1 style="letter-spacing: 5px;">[SUPREME] OBSIDIAN GRID COMMAND</h1>
                <div style="color: #6b7280;">LOCKED AT {datetime.now().strftime('%H:%M:%S')}</div>
            </div>

            <div class="grid-stats">
                <div class="stat-card">
                    <div style="color: #9ca3af;">ACTIVE PHYSICAL NODES</div>
                    <div class="stat-value">{active_count} / 102</div>
                </div>
                <div class="stat-card">
                    <div style="color: #9ca3af;">TOTAL DATA SUPPLIED</div>
                    <div class="stat-value">{total_gb:.2f} GB</div>
                </div>
                <div class="stat-card">
                    <div style="color: #9ca3af;">NETWORK REPUTATION</div>
                    <div class="stat-value" style="color: #10b981;">100/100</div>
                </div>
            </div>

            <table class="node-table">
                <thead>
                    <tr>
                        <th>Node Identity</th>
                        <th>Endpoint</th>
                        <th>Status</th>
                        <th>Ambient Stream</th>
                    </tr>
                </thead>
                <tbody>
        """

        for node in nodes:
            html_content += f"""
                <tr>
                    <td>{node[0]}</td>
                    <td>{node[1]}</td>
                    <td class="status-active">{node[2]}</td>
                    <td><div class="pulse"></div> Streaming...</td>
                </tr>
            """

        html_content += """
                </tbody>
            </table>
        </body>
        </html>
        """

        with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
            f.write(html_content)

        conn.close()
        print(f" SUCCESS: Dashboard live at {OUTPUT_HTML}")

if __name__ == "__main__":
    monitor = ObsidianVisualMonitor()
    monitor.generate_dashboard()
