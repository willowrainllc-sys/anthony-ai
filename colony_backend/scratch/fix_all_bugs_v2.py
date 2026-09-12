import os
import sqlite3
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
BACKEND = ROOT / "colony_backend"
DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def fix():
    print("=== 🔱 SUPREME BUG FIX: REPAIRING THE SOCIAL HUD CHAIN ===\n")

    # 1. Fix Class Name Syntax across the grid
    # Some rebrands left spaces like 'class Anthony Christopher'
    for f in BACKEND.glob("anthony_*.py"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content.replace("class Anthony Christopher", "class AnthonyChristopher")
            new_content = new_content.replace("Anthony ChristopherDaemon", "AnthonyChristopherDaemon")
            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] FIXED CLASS DNA: {f.name}")
        except: pass

    # 2. Fix the missing virtual_nodes table in the visual monitor
    # The monitor is crashing because the table doesn't exist in the current session
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
    conn.commit()
    conn.close()
    print("  [✓] DB SCHEMA: virtual_nodes table verified.")

    # 3. Reset stalled production jobs
    # If videos are not pushing, they might be stuck in 'EDITING'
    conn = sqlite3.connect(DB_PATH)
    conn.execute("UPDATE production_jobs SET status='QUEUED' WHERE status IN ('GENERATING', 'EDITING')")
    conn.commit()
    conn.close()
    print("  [✓] PRODUCTION: Stalled video jobs reset to QUEUED.")

if __name__ == "__main__":
    fix()
