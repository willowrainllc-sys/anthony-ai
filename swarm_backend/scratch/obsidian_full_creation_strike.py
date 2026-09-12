import os
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
APP_SRC = ROOT / "app" / "src" / "main" / "java"
OLD_PKG_PATH = APP_SRC / "com" / "example" / "anthony_ai"
NEW_PKG_PATH = APP_SRC / "com" / "obsidian" / "global"

REPLACEMENTS = {
    "com.example.anthony_ai": "com.obsidian.global",
    "Theme.Anthony_Ai": "Theme.Obsidian_Global",
    "Anthony_AiTheme": "Obsidian_GlobalTheme"
}

def full_creation_strike():
    print("=== 🔱 OBSIDIAN FULL CREATION: REWRITING THE WORLD DNA ===\n")

    # 1. Update File Contents (Packages and Themes)
    print("[*] Recoding Android source files...")
    for f in ROOT.rglob("*"):
        if f.is_file() and f.suffix in [".kt", ".xml", ".kts", ".gradle"]:
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                new_content = content
                for old, new in REPLACEMENTS.items():
                    new_content = new_content.replace(old, new)

                if new_content != content:
                    f.write_text(new_content, encoding='utf-8')
                    print(f"  [✓] DNA RECODED: {f.name}")
            except: pass

    # 2. Move Package Directory
    print(f"[*] Shifting physical hardware from {OLD_PKG_PATH.relative_to(ROOT)} to {NEW_PKG_PATH.relative_to(ROOT)}...")
    if OLD_PKG_PATH.exists():
        os.makedirs(NEW_PKG_PATH.parent, exist_ok=True)
        if NEW_PKG_PATH.exists():
            shutil.rmtree(NEW_PKG_PATH)
        shutil.move(str(OLD_PKG_PATH), str(NEW_PKG_PATH))
        print("  [✓] HARDWARE SHIFT COMPLETE.")

    # 3. Rename Theme function if it exists (usually in Theme.kt)
    # This is handled by the content replacement above

    print("\n🪐 FULL CREATION COMPLETE: Your World is now OBSIDIAN GLOBAL.")
    print("✓ Package: com.obsidian.global")
    print("✓ Theme: Theme.Obsidian_Global")

if __name__ == "__main__":
    full_creation_strike()
