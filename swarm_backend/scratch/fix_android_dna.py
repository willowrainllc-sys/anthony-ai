import os
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\app\src\main")

REPLACEMENTS = {
    "SaturnCarrierService": "ObsidianCarrierService",
    "SovereignAutopilotService": "ObsidianAutopilotService",
    "Sovereign": "Obsidian",
    "Saturn": "Obsidian",
    "spectrum": "obsidian_global"
}

def fix_android():
    print("=== 🔱 ANDROID DNA FIX: OBSIDIAN GLOBAL REBIRTH ===\n")
    for f in ROOT.rglob("*"):
        if f.is_file() and f.suffix in [".kt", ".xml"]:
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                new_content = content
                for old, new in REPLACEMENTS.items():
                    new_content = new_content.replace(old, new)

                if new_content != content:
                    f.write_text(new_content, encoding='utf-8')
                    print(f"  [✓] UPDATED: {f.name}")
            except Exception as e:
                print(f"  [-] ERROR {f.name}: {e}")

if __name__ == "__main__":
    fix_android()
