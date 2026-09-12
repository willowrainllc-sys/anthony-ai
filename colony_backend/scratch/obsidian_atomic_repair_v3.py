import os
import re
import sqlite3
from pathlib import Path

# Paths
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
BACKEND = ROOT / "colony_backend"
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
        new_content = new_content.replace('Anthony ChristopherIngressEngine', 'AnthonyChristopherIngressEngine')

        # 3. Fix broken imports after rebrand
        new_content = new_content.replace('from obsidian_persistence_engine', 'from anthony_persistence_engine')
        new_content = new_content.replace('import obsidian_persistence_engine', 'import anthony_persistence_engine')
        new_content = new_content.replace('import obsidian_ingress_data_flow_auditor', 'from obsidian_ingress_data_flow_auditor')

        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            return True
    except Exception as e:
        print(f"  [-] Error repairing {file_path.name}: {e}")
    return False

def setup_database():
    """Hardens the Empire Vault schema."""
    print("[*] Hardening Database Schema...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA journal_mode=WAL")

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

        # Add 'title' column to production_jobs if it's missing
        cursor = conn.execute("PRAGMA table_info(production_jobs)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'title' not in columns:
            print("[*] Adding 'title' column to production_jobs...")
            conn.execute("ALTER TABLE production_jobs ADD COLUMN title TEXT")

        # Seed the The Nest
        for port in range(1080, 1183):
            conn.execute("INSERT OR IGNORE INTO virtual_nodes (node_id, status) VALUES (?, 'GATHERING')", (f"OBS-IND-{port}",))

        conn.commit()
        print("  [✓] DB Integrity Locked.")
    except Exception as e:
        print(f"  [-] DB Setup Error: {e}")
    finally:
        conn.close()

def main():
    print("=== 🔱 OBSIDIAN ATOMIC REPAIR v3: STABILIZING THE MACHINE ===\n")

    count = 0
    for folder in [BACKEND, INGRESS, CELLULAR]:
        if not folder.exists(): continue
        for f in folder.glob("*.py"):
            if repair_file_content(f):
                print(f"  [✓] REPAIRED: {f.name}")
                count += 1

    setup_database()
    print(f"\n🪐 REPAIR COMPLETE: {count} files fixed. System is stable.")

if __name__ == "__main__":
    main()
