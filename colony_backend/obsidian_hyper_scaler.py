# --- WILLOW RAIN SECURITY: OBSIDIAN HYPER-SCALER v12.0 (PRODUCTION REALITY) ---
import asyncio
import os
import uuid
import time
import socket
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

class ObsidianHyperScaler:
    """
    OBSIDIAN HYPER-SCALER v12.0:
    PRODUCTION REALITY ENGINE.
    1. PHYSICAL PORT AUDIT: Instead of generating fake IPs, it pings the local matrix ports (8000, 1080-1180).
    2. LIVE REGISTRATION: Only registers ports that are physically OPEN and listening.
    3. REVENUE FOCUS: Ensures each active port is mapped to a master account in the ledger.
    """
    def __init__(self):
        self.master_port = 8000
        self.colony_ports = list(range(1080, 1181))

    def _is_port_open(self, port: int) -> bool:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.1)
            return s.connect_ex(('127.0.0.1', port)) == 0

    async def execute_industrial_expansion(self):
        colony_log("HYPER_SCALER: Auditing physical matrix for production readiness...", node="SUPREME")

        active_ports = []
        # Audit Master Port
        if self._is_port_open(self.master_port):
            active_ports.append(self.master_port)

        # Audit Colony Ports
        for p in self.colony_ports:
            if self._is_port_open(p):
                active_ports.append(p)

        colony_log(f"HYPER_SCALER: Found {len(active_ports)} physically OPEN residential ports.", node="SUPREME")

        # Sync with Obsidian Registry
        for port in active_ports:
            node_id = f"FEEDER-PHY-{port}"
            # Unique Ghost identity for each physical port
            with db._get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO virtual_nodes (node_id, account_email, proxy_endpoint, service, status, last_pulse)
                    VALUES (?, ?, ?, ?, 'GATHERING', ?)
                """, (node_id, "obsidian.global.holdings@gmail.com", f"socks5://127.0.0.1:{port}", "OBSIDIAN_INGRESS", time.time()))
                conn.commit()

        colony_log(f"[SUPREME] SUPREME SUCCESS: {len(active_ports)} REAL nodes synchronized. No simulations active.", node="SUPREME")
        return len(active_ports)

hyper_scaler = ObsidianHyperScaler()

if __name__ == "__main__":
    asyncio.run(hyper_scaler.execute_industrial_expansion())
