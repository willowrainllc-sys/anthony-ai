import sqlite3
import os

db_path = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def fix():
    print("=== 🔱 DATABASE REPAIR: RESTORING VIRTUAL_NODES ===\n")
    conn = sqlite3.connect(db_path)

    # Create the table properly
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

    # Register the physical phone and matrix slots
    host_ip = "192.168.1.214"
    conn.execute("""
        INSERT OR REPLACE INTO virtual_nodes (node_id, account_email, proxy_endpoint, service, status, last_pulse)
        VALUES (?, ?, ?, ?, 'GATHERING', ?)
    """, ("MASTER-PHONE-01", "saturn.global.holdings@gmail.com", f"socks5://{host_ip}:8000", "OBSIDIAN_INGRESS", 0))

    conn.commit()
    conn.close()
    print("✓ SUCCESS: virtual_nodes table is ARMED.")

if __name__ == "__main__":
    fix()
