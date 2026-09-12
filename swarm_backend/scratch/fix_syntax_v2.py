import os
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend")

def fix():
    # 1. Fix obsidian_obsidian_bridge_autoclaim.py instantiation
    f1 = ROOT / "obsidian_obsidian_bridge_autoclaim.py"
    if f1.exists():
        content = f1.read_text(encoding='utf-8')
        new_content = content.replace("class Obsidian BridgeAutoClaimEngine:", "class ObsidianBridgeAutoClaimEngine:")
        new_content = new_content.replace("jmpt_autoclaim = Obsidian BridgeAutoClaimEngine()", "jmpt_autoclaim = ObsidianBridgeAutoClaimEngine()")
        f1.write_text(new_content, encoding='utf-8')
        print(f"  [✓] FIXED: {f1.name}")

    # 2. Fix anthony_persistence_engine.py class name
    f2 = ROOT / "anthony_persistence_engine.py"
    if f2.exists():
        content = f2.read_text(encoding='utf-8')
        new_content = content.replace("class Anthony ChristopherPersistenceEngine:", "class AnthonyChristopherPersistenceEngine:")
        f2.write_text(new_content, encoding='utf-8')
        print(f"  [✓] FIXED: {f2.name}")

    # 3. Create missing virtual_nodes table if it disappeared
    db_path = r'C:\AnthonyAi_Swarm\Empire_Vault.db'
    import sqlite3
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS virtual_nodes (
            node_id TEXT PRIMARY KEY,
            account_email TEXT,
            proxy_endpoint TEXT,
            service TEXT,
            status TEXT,
            last_pulse REAL
        )
    """)
    conn.commit()
    conn.close()
    print("  [✓] DB SCHEMA: virtual_nodes verified.")

if __name__ == "__main__":
    fix()
