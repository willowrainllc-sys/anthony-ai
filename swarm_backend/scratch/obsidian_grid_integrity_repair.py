import sqlite3
import os
import time

db_path = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def repair():
    print("=== 🔱 OBSIDIAN GRID REPAIR: RESTORING THE HIVE ===\n")
    if not os.path.exists(os.path.dirname(db_path)):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Restore Virtual Nodes Table
    print("[*] Re-birthing virtual_nodes table...")
    cur.execute("""
        CREATE TABLE IF NOT EXISTS virtual_nodes (
            node_id TEXT PRIMARY KEY,
            account_email TEXT,
            proxy_endpoint TEXT,
            service TEXT,
            status TEXT DEFAULT 'GATHERING',
            last_pulse REAL
        )
    """)

    # 2. Re-register the 101 physical ports found in the last audit
    host_ip = "192.168.1.214"
    print("[*] Registering 101 physical ports into the hive...")
    for port in range(1080, 1181):
        node_id = f"OBS-PHY-{port}"
        cur.execute("""
            INSERT OR REPLACE INTO virtual_nodes (node_id, account_email, proxy_endpoint, service, status, last_pulse)
            VALUES (?, ?, ?, ?, 'GATHERING', ?)
        """, (node_id, "saturn.global.holdings@gmail.com", f"socks5://{host_ip}:{port}", "OBSIDIAN_INGRESS", time.time()))

    # 3. Add Master Phone
    cur.execute("""
        INSERT OR REPLACE INTO virtual_nodes (node_id, account_email, proxy_endpoint, service, status, last_pulse)
        VALUES (?, ?, ?, ?, 'GATHERING', ?)
    """, ("MASTER-PHONE-PRO", "saturn.global.holdings@gmail.com", "MOBILE_DATA", "OBSIDIAN_INGRESS", time.time()))

    conn.commit()
    conn.close()
    print("\n✓ SUCCESS: Grid Integrity Restored. 102 Nodes Registered.")

if __name__ == "__main__":
    repair()
