# --- WILLOW RAIN SECURITY: OBSIDIAN AUTO-RUN & REBOOT RECOVERY v1.0 ---
import os
import winshell
from win32com.client import Dispatch
from pathlib import Path

def setup_autorun():
    print("=== [SUPREME] OBSIDIAN REBOOT RECOVERY SETUP ===\n")

    # 1. Define Paths
    base_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai")
    launcher_py = base_dir / "swarm_backend" / "obsidian_production_launcher.py"
    startup_folder = winshell.startup()
    shortcut_path = os.path.join(startup_folder, "WillowRain_Grid_Launcher.lnk")

    # 2. Create the Shortcut
    print(f"[*] Creating recovery shortcut in Windows Startup...")
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)

    # We run the python script directly
    shortcut.TargetPath = "python.exe"
    shortcut.Arguments = str(launcher_py)
    shortcut.WorkingDirectory = str(base_dir)
    shortcut.IconLocation = "python.exe"
    shortcut.Description = "Willow Rain Security Grid Auto-Ignition"
    shortcut.save()

    print(f"\n SETUP SUCCESS: The Obsidian Grid will now auto-ignite on computer startup.")
    print(f"Location: {shortcut_path}")

if __name__ == "__main__":
    try: setup_autorun()
    except Exception as e: print(f"[-] Setup Error: {e}")
