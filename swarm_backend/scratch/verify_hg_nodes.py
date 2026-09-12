import sqlite3
import time

def verify():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    rows = conn.execute("SELECT node_id, status, last_pulse FROM virtual_nodes WHERE service='OBSIDIAN_INGRESS'").fetchall()

    print(f"Total Registered Obsidian Ingress Nodes: {len(rows)}")

    now = time.time()
    active_count = 0
    stalled_count = 0

    for r in rows:
        # Check if pulsed in last 10 minutes (600 seconds)
        if (now - r[2]) < 600:
            active_count += 1
        else:
            stalled_count += 1

    print(f"Active (Gathering): {active_count}")
    print(f"Stalled (No recent pulse): {stalled_count}")

    conn.close()

if __name__ == "__main__":
    verify()
