import sqlite3
import os
import time

db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
host_ip = "192.168.1.214"

def register():
    print("🔱 REGISTERING FAMILY DEVICES TO SOVEREIGN GRID...")
    conn = sqlite3.connect(db_path)

    # 1. Lily's Phone (314-780-0938)
    conn.execute("""
        INSERT OR REPLACE INTO virtual_nodes (node_id, account_email, proxy_endpoint, service, status, last_pulse)
        VALUES (?, ?, ?, ?, 'GATHERING', ?)
    """, ("LILY-PHONE-1085", "lilydiane1995@gmail.com", f"socks5://{host_ip}:1085", "OBSIDIAN_INGRESS", time.time()))

    # 2. Register slots for the other 10 devices on separate ports
    for i in range(1, 11):
        port = 1085 + i
        node_id = f"FAMILY-DEVICE-{i}"
        conn.execute("""
            INSERT OR REPLACE INTO virtual_nodes (node_id, account_email, proxy_endpoint, service, status, last_pulse)
            VALUES (?, ?, ?, ?, 'GATHERING', ?)
        """, (node_id, "obsidian.global.holdings@gmail.com", f"socks5://{host_ip}:{port}", "OBSIDIAN_INGRESS", time.time()))

    conn.commit()
    conn.close()
    print("✓ SUCCESS: 11 Family Devices mapped to the Sovereign Matrix.")

if __name__ == "__main__":
    register()
