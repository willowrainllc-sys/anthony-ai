import os
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\colony_backend")

TARGETS = [
    "obsidian_brain_server.py",
    "obsidian_brain_gate.py",
    "obsidian_command_bridge.py",
    "obsidian_daemon_core.py",
    "obsidian_persistence_engine.py",
    "obsidian_command_os.py",
    "obsidian_sub_ai_kernel.py",
    "obsidian_agent_bridge.py",
    "Modelfile_Obsidian_Christopher.0"
]

def restore():
    print("=== 🔱 RESTORING ANTHONY'S DAEMONS: THE BRAIN IDENTITY ===\n")
    for old_name in TARGETS:
        f = ROOT / old_name
        if f.exists():
            new_name = old_name.replace("obsidian", "anthony").replace("Obsidian", "Anthony")
            try:
                os.rename(f, ROOT / new_name)
                print(f"  [✓] RESTORED: {old_name} -> {new_name}")
            except Exception as e:
                print(f"  [-] ERROR: {old_name} -> {e}")

    # Now update the content of these specific files to use 'Anthony' for the AI identity
    for f in ROOT.glob("anthony_*.py"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content.replace("Obsidian", "Anthony Christopher").replace("obsidian", "anthony")
            f.write_text(new_content, encoding='utf-8')
        except: pass

if __name__ == "__main__":
    restore()
