# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN PORTABLE VAULT & AUTO-IGNITER v1.0 ---
import os
import shutil
import subprocess
from pathlib import Path

SOURCE_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
DRIVE_E = Path("E:/")

def create_portable_vault():
    print(f"🔱 Initiating Portable Vault Construction on Drive E:...")

    if not DRIVE_E.exists():
        print("[-] ERROR: Drive E: not detected. Plug in the thumb drive.")
        return

    # 1. Wipe the drive (Purge legacy Windows files)
    print("[*] PURGING: Reclaiming space for the Obsidian Mesh...")
    for item in DRIVE_E.iterdir():
        try:
            if item.is_dir(): shutil.rmtree(item)
            else: item.unlink()
        except Exception as e:
            print(f"    [!] Skip {item.name}: {e}")

    # 2. Create Empire Directory
    vault_path = DRIVE_E / "Obsidian_Empire"
    vault_path.mkdir(exist_ok=True)

    # 3. Sync Core Project (Excluding heavy venv/git)
    print("[*] SYNCING: Copying core DNA to vault...")
    ignore_list = shutil.ignore_patterns('.git', 'venv', '__pycache__', 'app/build', '.gradle')
    shutil.copytree(SOURCE_DIR, vault_path, ignore=ignore_list, dirs_exist_ok=True)

    # 4. Create the 'IGNITE_COLONY.bat' Master Trigger
    # This script will be on the root of the thumb drive
    ignite_script = DRIVE_E / "IGNITE_COLONY.bat"
    script_content = f"""@echo off
title 🔱 OBSIDIAN COLONY: PORTABLE IGNITER
echo 🔱 Initiating Global Ingress from Portable Vault...
cd /d "%~dp0Obsidian_Empire"

:: 1. Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [-] Python not found. Initiating Emergency Download...
    start https://www.python.org/downloads/
    pause
    exit
)

:: 2. Setup / Sync Environment
echo [*] SYNCING: Verifying environment integrity...
if not exist venv (
    echo [+] CREATING: Bootstrapping new virtual node...
    python -m venv venv
)

:: 3. Execute Self-Healing (ARES MASTER FIXER)
echo 🔱 ARES: Running deep-system self-healing...
venv\\Scripts\\python.exe colony_backend\\ares_master_empire_fixer.py

:: 4. Status Check
echo 🔱 COLONY: Verifying global node telemetry...
venv\\Scripts\\python.exe colony_backend\\colony_status_report.py

echo [+] MISSION READY: The Empire is now active on this host.
pause
"""
    ignite_script.write_text(script_content, encoding="utf-8")

    print("\n" + "="*70)
    print("  🔱 PORTABLE VAULT READY")
    print("  DRIVE: E:")
    print("  ACTION: Plug into any PC and run 'IGNITE_COLONY.bat'")
    print("  ARES will handle the rest: Auto-Setup, Self-Healing, and Sync.")
    print("="*70 + "\n")

if __name__ == "__main__":
    create_portable_vault()
