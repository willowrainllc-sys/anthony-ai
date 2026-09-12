import os
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
BACKEND = ROOT / "swarm_backend"

REPLACEMENTS = {
    "anthony-engine run": "anthony-engine run",
    "anthony-engine list": "anthony-engine list",
    "anthony-engine create": "anthony-engine create",
    "anthony-engine rm": "anthony-engine rm",
    "anthony-engine cp": "anthony-engine cp"
}

def hide_legacy_name():
    print("=== 🔱 OBSIDIAN ENGINE HIDDEN: DELETING OLLAMA STRINGS ===\n")
    update_count = 0

    for f in BACKEND.rglob("*.py"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content
            for old, new in REPLACEMENTS.items():
                new_content = new_content.replace(old, new)

            # Special case for the server
            if f.name == "anthony_brain_server.py":
                 new_content = new_content.replace("f'anthony-engine run {self.primary_model}", "f'anthony-engine run {self.primary_model}")

            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] HIDDEN OLLAMA: {f.name}")
                update_count += 1
        except: pass

    # Also update .bat files
    for f in ROOT.glob("*.bat"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            new_content = content
            for old, new in REPLACEMENTS.items():
                new_content = new_content.replace(old, new)
            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] HIDDEN OLLAMA: {f.name}")
                update_count += 1
        except: pass

    print(f"\n🪐 OLLAMA INCINERATED: {update_count} files transitioned to ANTHONY-ENGINE.")

if __name__ == "__main__":
    hide_legacy_name()
