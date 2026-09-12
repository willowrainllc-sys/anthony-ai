import sqlite3

def run():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    rows = conn.execute("SELECT event_type, COUNT(*) FROM empire_events GROUP BY event_type").fetchall()

    print("\n=== 🔱 LIFETIME GRID TELEMETRY ===")
    for r in rows:
        print(f"- {r[0]}: {r[1]}")
    conn.close()

if __name__ == "__main__":
    run()
