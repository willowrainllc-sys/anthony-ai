import os
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
BACKEND = ROOT / "swarm_backend"
DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def fix_imports():
    print("[*] Fixing import references to Anthony Persistence Engine...")
    for f in BACKEND.glob("*.py"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content.replace("from obsidian_persistence_engine", "from anthony_persistence_engine")
            new_content = new_content.replace("import obsidian_persistence_engine", "import anthony_persistence_engine")
            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] FIXED: {f.name}")
        except: pass

def fix_db():
    print("[*] Ensuring Empire Vault schema is complete...")
    conn = sqlite3.connect(DB_PATH)
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
    # Register the 103 current nodes if missing
    for port in range(1080, 1183):
        conn.execute("INSERT OR IGNORE INTO virtual_nodes (node_id, status) VALUES (?, 'GATHERING')", (f"OBS-IND-{port}",))
    conn.commit()
    conn.close()
    print("  [✓] DB SCHEMA: virtual_nodes verified.")

if __name__ == "__main__":
    fix_imports()
    fix_db()
