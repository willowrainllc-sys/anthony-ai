import os
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
BACKEND = ROOT / "swarm_backend"
DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def fix_python_syntax():
    print("=== 🔱 BUG FIX STRIKE: INCINERATING SYNTAX ERRORS ===\n")

    # Files to fix
    targets = {
        "anthony_persistence_engine.py": [
            ("class Anthony ChristopherPersistenceEngine:", "class AnthonyChristopherPersistenceEngine:"),
            ("persistence_engine = Anthony ChristopherPersistenceEngine()", "persistence_engine = AnthonyChristopherPersistenceEngine()")
        ],
        "anthony_daemon_core.py": [
            ("class Anthony ChristopherDaemonCore", "class AnthonyChristopherDaemonCore"),
            ("from anthony_daemon_base import Anthony ChristopherDaemon", "from anthony_daemon_base import AnthonyChristopherDaemon"),
            ("core = Anthony ChristopherDaemonCore()", "core = AnthonyChristopherDaemonCore()")
        ],
        "anthony_command_bridge.py": [
            ("class Anthony ChristopherCommandBridge:", "class AnthonyChristopherCommandBridge:")
        ],
        "anthony_command_os.py": [
            ("class Anthony ChristopherCommandOS:", "class AnthonyChristopherCommandOS:"),
            ("grid_os = Anthony ChristopherCommandOS()", "grid_os = AnthonyChristopherCommandOS()")
        ]
    }

    for filename, reps in targets.items():
        f = BACKEND / filename
        if f.exists():
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content
            for old, new in reps:
                new_content = new_content.replace(old, new)

            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] FIXED SYNTAX: {filename}")

def fix_database():
    print("\n[*] Auditing Database Schema...")
    conn = sqlite3.connect(DB_PATH)
    try:
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
        # Ensure we have at least the Master Phone registered
        conn.execute("INSERT OR IGNORE INTO virtual_nodes (node_id, account_email, status) VALUES ('MASTER-PIXEL-PRO', 'saturn.global.holdings@gmail.com', 'ACTIVE')")
        conn.commit()
        print("  [✓] DB SCHEMA: virtual_nodes table verified.")
    except Exception as e:
        print(f"  [-] DB ERROR: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    fix_python_syntax()
    fix_database()
