import sqlite3
import os
import sys

# Fix path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'

def audit():
    if not os.path.exists(db_path):
        print("Database not found.")
        return

    conn = sqlite3.connect(db_path)
    # Correct table is swarm_tasks
    rows = conn.execute("SELECT channel, COUNT(*) FROM swarm_tasks WHERE status='NEGOTIATING' GROUP BY channel").fetchall()

    print("=== 🔱 SWARM TASK QUEUE AUDIT ===\n")
    if not rows:
        print("No negotiating tasks found.")
    else:
        for r in rows:
            print(f"Channel: {r[0]} | Negotiating Tasks: {r[1]}")

    # Check for recent failures
    fails = conn.execute("SELECT channel, error_log FROM swarm_tasks WHERE status='FAILED' ORDER BY id DESC LIMIT 5").fetchall()
    if fails:
        print("\n--- RECENT FAILURES ---")
        for f in fails:
            print(f"Channel: {f[0]} | Error: {str(f[1])[:150]}...")

    conn.close()

if __name__ == "__main__":
    audit()
