import sqlite3

def audit():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    rows = conn.execute("SELECT node_id FROM virtual_nodes").fetchall()

    virtual_swarm = 0
    matrix_ports = 0

    for r in rows:
        if "FEEDER-A" in r[0] or "V-SWARM" in r[0]:
            virtual_swarm += 1
        elif "FEEDER-IP" in r[0]:
            matrix_ports += 1

    print("=== 🔱 NODE COMPOSITION AUDIT ===")
    print(f"Total Nodes: {len(rows)}")
    print(f"Virtual Docker/Process Flows: {virtual_swarm}")
    print(f"Dedicated Matrix Ports: {matrix_ports}")

    conn.close()

if __name__ == "__main__":
    audit()
