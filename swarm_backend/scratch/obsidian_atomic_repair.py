import os
import re
import sqlite3
from pathlib import Path

# Paths
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
BACKEND = ROOT / "swarm_backend"
INGRESS = ROOT / "willow_rain_global" / "ingress_api"
CELLULAR = ROOT / "willow_rain_global" / "cellular_stack"
DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def repair_file_content(file_path):
    """Surgically repairs syntax and import errors in a single file."""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')

        # 1. Fix Class Names with spaces
        new_content = re.sub(r'class\s+Anthony\s+Christopher(\w+):', r'class AnthonyChristopher\1:', content)
        new_content = re.sub(r'class\s+Obsidian\s+Bridge(\w+):', r'class ObsidianBridge\1:', content)

        # 2. Fix variable/instance names with spaces
        new_content = new_content.replace('Anthony ChristopherDaemon', 'AnthonyChristopherDaemon')
        new_content = new_content.replace('Anthony ChristopherPersistenceEngine', 'AnthonyChristopherPersistenceEngine')
        new_content = new_content.replace('Obsidian BridgeAutoClaimEngine', 'ObsidianBridgeAutoClaimEngine')
        new_content = new_content.replace('Anthony ChristopherCommandOS', 'AnthonyChristopherCommandOS')

        # 3. Fix broken imports after rebrand
        # Ensure imports point to existing filenames
        new_content = new_content.replace('from obsidian_persistence_engine', 'from anthony_persistence_engine')
        new_content = new_content.replace('import obsidian_persistence_engine', 'import anthony_persistence_engine')

        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            return True
    except Exception as e:
        print(f"  [-] Error repairing {file_path.name}: {e}")
    return False

def setup_database():
    """Ensures all required tables exist in the vault."""
    print("[*] Hardening Database Schema...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        # Virtual Nodes (The Grid)
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

        # Payout Tasks
        conn.execute("""
            CREATE TABLE IF NOT EXISTS swarm_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at REAL,
                channel TEXT,
                payload TEXT,
                status TEXT DEFAULT 'NEGOTIATING',
                error_log TEXT
            )
        """)

        # Production Jobs (Videos)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS production_jobs (
                job_id TEXT PRIMARY KEY,
                title TEXT,
                status TEXT,
                progress INTEGER,
                current_stage TEXT,
                manifest TEXT,
                updated_at REAL
            )
        """)

        conn.commit()
        print("  [✓] DB Integrity Verified.")
    except Exception as e:
        print(f"  [-] DB Setup Error: {e}")
    finally:
        conn.close()

def main():
    print("=== 🔱 OBSIDIAN ATOMIC REPAIR: REBIRTHING THE ENGINE ===\n")

    # Repair all python files in core directories
    count = 0
    for folder in [BACKEND, INGRESS, CELLULAR]:
        if not folder.exists(): continue
        for f in folder.glob("*.py"):
            if repair_file_content(f):
                print(f"  [✓] REPAIRED: {f.name}")
                count += 1

    setup_database()
    print(f"\n🪐 ATOMIC REPAIR COMPLETE: {count} files fixed. System is stable.")

if __name__ == "__main__":
    main()
