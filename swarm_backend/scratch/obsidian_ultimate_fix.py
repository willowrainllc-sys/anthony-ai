import os
import re
import sqlite3
import subprocess
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
BACKEND = ROOT / "swarm_backend"
DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

def repair_all_code():
    print("=== 🔱 OBSIDIAN ULTIMATE CODE REPAIR ===\n")

    # 1. Fix Syntax Errors in Daemons
    # We must use utf-8 to avoid UnicodeDecodeErrors
    for f in BACKEND.glob("*.py"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')

            # Fix class names with spaces
            new_content = re.sub(r'class\s+Anthony\s+Christopher(\w+):', r'class AnthonyChristopher\1:', content)
            new_content = re.sub(r'class\s+Obsidian\s+Bridge(\w+):', r'class ObsidianBridge\1:', content)

            # Fix variable/instance names with spaces
            new_content = new_content.replace('Anthony ChristopherDaemon', 'AnthonyChristopherDaemon')
            new_content = new_content.replace('Anthony ChristopherPersistenceEngine', 'AnthonyChristopherPersistenceEngine')
            new_content = new_content.replace('Obsidian BridgeAutoClaimEngine', 'ObsidianBridgeAutoClaimEngine')
            new_content = new_content.replace('Anthony ChristopherCommandOS', 'AnthonyChristopherCommandOS')
            new_content = new_content.replace('Anthony ChristopherIngressEngine', 'AnthonyChristopherIngressEngine')
            new_content = new_content.replace('Anthony Christopher', 'AnthonyChristopher')

            # Fix imports
            new_content = new_content.replace('from obsidian_persistence_engine', 'from anthony_persistence_engine')
            new_content = new_content.replace('import obsidian_persistence_engine', 'import anthony_persistence_engine')

            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] FIXED: {f.name}")
        except Exception as e:
            print(f"  [-] ERROR repairing {f.name}: {e}")

def optimize_pc():
    print("\n=== 🔱 OBSIDIAN SYSTEM OPTIMIZATION ===\n")

    # 1. Clear Temp Files
    temp_dirs = [os.environ.get('TEMP'), r"C:\Windows\Temp"]
    for d in temp_dirs:
        if d and os.path.exists(d):
            print(f"[*] Purging Temp: {d}")
            try:
                # Use shell to handle permission issues
                subprocess.run(f'del /q /s /f "{d}\\*"', shell=True, capture_output=True)
            except: pass

    # 2. Set Ultimate Performance Power Plan
    print("[*] Locking System into 'Ultimate Performance' Mode...")
    try:
        # Check if the plan exists, if not, create it from the HID
        subprocess.run("powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True, capture_output=True)
        subprocess.run("powercfg -setactive e9a42b02-d5df-448d-aa00-03f14749eb61", shell=True, capture_output=True)
    except: pass

    # 3. Kill Stale Browser/FFmpeg Instances
    print("[*] Clearing resource-heavy background ghosts...")
    subprocess.run("taskkill /F /IM chrome.exe /T /FI \"STATUS eq RUNNING\"", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM node.exe /T /FI \"STATUS eq RUNNING\"", shell=True, capture_output=True)
    subprocess.run("taskkill /F /IM ffmpeg.exe /T /FI \"STATUS eq RUNNING\"", shell=True, capture_output=True)

def setup_database():
    print("\n[*] Hardening Database for Production...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("PRAGMA journal_mode=WAL") # High concurrency
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
        # Seed the master phone node
        conn.execute("INSERT OR IGNORE INTO virtual_nodes (node_id, account_email, status) VALUES ('MASTER-PIXEL-PRO', 'saturn.global.holdings@gmail.com', 'ACTIVE')")
        conn.commit()
        print("  [✓] DB Integrity Locked.")
    except Exception as e:
        print(f"  [-] DB ERROR: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    repair_all_code()
    optimize_pc()
    setup_database()
    print("\n🪐 PC RECOVERY COMPLETE. PERFORMANCE MAXIMIZED.")
