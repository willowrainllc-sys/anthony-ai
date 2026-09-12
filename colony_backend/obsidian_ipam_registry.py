# --- WILLOW RAIN SECURITY: OBSIDIAN IPAM (IP ADDRESS MANAGEMENT) v1.0 ---
import os
import json
import sqlite3
import time
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

class ObsidianIPAM:
    """
    OBSIDIAN IPAM v1.0:
    The "Data Center" Intelligence for the Ghost Fleet.
    1. POOL MANAGEMENT: Manages the 5,000+ unique public IPs as a managed asset.
    2. DHCP EMULATOR: Automatically "Leases" a unique IP to each virtual phone.
    3. COLLISION PREVENTION: Ensures 100% adherence to the "1 Device Per IP" rule.
    4. REPUTATION TRACKING: Maps every IP to its ISP reputation score (100/100 target).
    """
    def __init__(self):
        self._init_db()

    def _init_db(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ip_pool (
                    ip_address TEXT PRIMARY KEY,
                    provider TEXT,
                    ip_type TEXT DEFAULT 'RESIDENTIAL', -- 'ISP', 'MOB', 'DCH'
                    is_cd_eligible BOOLEAN DEFAULT 0,
                    lease_status TEXT DEFAULT 'AVAILABLE',
                    assigned_node_id TEXT,
                    reputation_score INTEGER DEFAULT 100,
                    last_audit REAL
                )
            """)
            conn.commit()

    def lease_ip(self, node_id: str) -> str:
        """Acts like a DHCP server: Hands out the next available public IP."""
        with db._get_connection() as conn:
            # Find an available IP
            row = conn.execute("SELECT ip_address FROM ip_pool WHERE lease_status='AVAILABLE' LIMIT 1").fetchone()

            if not row:
                colony_log(f"[ALERT] IPAM: No AVAILABLE IPs in pool. Capacity breached.", node="SECURITY")
                return None

            ip = row[0]
            conn.execute("""
                UPDATE ip_pool
                SET lease_status='LEASED', assigned_node_id=?, last_audit=?
                WHERE ip_address=?
            """, (node_id, time.time(), ip))
            conn.commit()

            colony_log(f" IPAM: Leased [{ip}] to Node [{node_id}].", node="SECURITY")
            return ip

    def release_ip(self, ip_address: str):
        """Returns an IP to the pool."""
        with db._get_connection() as conn:
            conn.execute("UPDATE ip_pool SET lease_status='AVAILABLE', assigned_node_id=NULL WHERE ip_address=?", (ip_address,))
            conn.commit()

    def add_to_pool(self, ip: str, provider: str):
        """Registers a new public IP from the Cloud Mesh into the Master Pool."""
        with db._get_connection() as conn:
            conn.execute("INSERT OR IGNORE INTO ip_pool (ip_address, provider) VALUES (?, ?)", (ip, provider))
            conn.commit()

    def get_pool_status(self) -> dict:
        with db._get_connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM ip_pool").fetchone()[0]
            leased = conn.execute("SELECT COUNT(*) FROM ip_pool WHERE lease_status='LEASED'").fetchone()[0]
        return {"total_ips": total, "leased": leased, "available": total - leased}

ipam = ObsidianIPAM()

if __name__ == "__main__":
    status = ipam.get_pool_status()
    print("\n=== [SUPREME] WILLOW RAIN IPAM STATUS ===\n")
    print(f"  Total Public IPs: {status['total_ips']}")
    print(f"  Active Leases:    {status['leased']}")
    print(f"  Available:        {status['available']}")
