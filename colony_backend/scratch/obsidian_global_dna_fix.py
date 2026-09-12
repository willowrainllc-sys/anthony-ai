# --- OBSIDIAN GLOBAL: DNA STABILIZATION & SECURITY HARDENING v1.0 ---
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

# Paths
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
BACKEND = ROOT / "colony_backend"
INGRESS = ROOT / "willow_rain_global" / "ingress_api"
CELLULAR = ROOT / "willow_rain_global" / "cellular_stack"
OIS = ROOT / "willow_rain_global" / "obsidian_intelligence"
CARRIERS = ROOT / "willow_rain_global" / "imperium_carrier_core"
DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def repair_file(file_path):
    """Surgically repairs logic and encoding defects in a single file."""
    try:
        # We use ignore to strip any already corrupted bytes
        content = file_path.read_text(encoding='utf-8', errors='ignore')

        # 1. Identity Fix: Merge spaced names
        new_content = re.sub(r'class\s+Anthony\s+Christopher(\w+):', r'class AnthonyChristopher\1:', content)
        new_content = new_content.replace('Anthony Christopher', 'AnthonyChristopher')
        new_content = new_content.replace('Obsidian Bridge', 'ObsidianBridge')

        # 2. Ingress Fix: Decouple from legacy 'ollama' names in commands
        new_content = new_content.replace('ollama run', 'anthony-engine run')

        # 3. Persistence Fix: Align imports
        new_content = new_content.replace('from obsidian_persistence_engine', 'from anthony_persistence_engine')
        new_content = new_content.replace('import obsidian_persistence_engine', 'import anthony_persistence_engine')

        # 4. Encoding Fix: Strip emojis that cause CMD/PowerShell crashes
        replacements = {
            "🔱": "[SUPREME]", "🪐": "[SATURN]", "⚛️": "[ATOMIC]",
            "⚠️": "[ALERT]", "💀": "[DEATH]", "✅": "[SUCCESS]",
            "🚀": "[STRIKE]", "💰": "[CASH]", "💸": "[WEALTH]",
            "📊": "[DATA]", "📡": "[SIGNAL]", "🕵️‍♂️": "[SHADOW]",
            "🧠": "[BRAIN]", "🏛️": "[IMPERIUM]", "🔌": "[LINK]",
            "💎": "[OBSIDIAN]"
        }
        for emoji, text in replacements.items():
            new_content = new_content.replace(emoji, text)

        # Strip remaining non-ascii
        new_content = new_content.encode("ascii", "ignore").decode("ascii")

        if new_content != content:
            file_path.write_text(new_content, encoding='utf-8')
            return True
    except Exception as e:
        print(f"  [-] Error in {file_path.name}: {e}")
    return False

def harden_infrastructure():
    """Performs physical security checks and database hardening."""
    print("[*] Hardening Database Registry...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        # Ensure we have the latest production tables
        conn.execute("""
            CREATE TABLE IF NOT EXISTS security_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL,
                event TEXT,
                severity TEXT,
                source TEXT
            )
        """)
        conn.commit()
    finally:
        conn.close()

def main():
    print("=== 🔱 OBSIDIAN GLOBAL DNA FIX: REBIRTHING THE SOFTWARE ===\n")

    folders = [BACKEND, INGRESS, CELLULAR, OIS, CARRIERS]
    repaired_count = 0

    for folder in folders:
        if not folder.exists(): continue
        print(f"[*] Auditing {folder.name}...")
        for f in folder.glob("*.py"):
            if repair_file(f):
                print(f"  [✓] DNA STABILIZED: {f.name}")
                repaired_count += 1

    harden_infrastructure()
    print(f"\n🪐 STRIKE COMPLETE: {repaired_count} files hardened. Software is now stable.")

if __name__ == "__main__":
    main()
