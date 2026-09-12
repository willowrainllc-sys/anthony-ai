import sqlite3
import os
import sys

# Fix path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'

def reset():
    print("=== 🔱 SUPREME PRODUCTION HARD RESET: NO MORE SIMULATIONS ===\n")

    if not os.path.exists(db_path):
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # 1. Clear Simulated Nodes
    print("[*] Incinerating 44,000+ simulated nodes...")
    cur.execute("DELETE FROM virtual_nodes")
    cur.execute("DELETE FROM ip_pool")

    # 2. Clear Fake Revenue Events
    print("[*] Purging simulated financial logs...")
    cur.execute("DELETE FROM empire_events WHERE event_type IN ('DATA_FLOW_AUDIT_COMPLETE', 'SUPREME_GHOST_WITHDRAWAL', 'REVENUE_BLITZ_PULSE', 'GRID_PERFORMANCE_AUDIT')")

    # 3. Keep verified authority nodes (127.0.0.1)
    print("[*] Re-initializing Master Authority Node...")
    # Add your local residential port
    cur.execute("""
        INSERT INTO virtual_nodes (node_id, account_email, proxy_endpoint, service, status, last_pulse)
        VALUES ('MASTER-AUTH-01', 'obsidian.global.holdings@gmail.com', 'socks5://127.0.0.1:8000', 'OBSIDIAN_INGRESS', 'GATHERING', 0)
    """)

    conn.commit()
    conn.close()
    print("\n✓ RESET COMPLETE: The grid is now clean. Only REAL data will be logged from this second.")

if __name__ == "__main__":
    reset()
