# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- REBRAND: LEO -> OBSIDIAN AI v1.0 ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# Mappings for Rebranding
mappings = {
    "Anthony AI the Supreme": "Anthony AI the Supreme",
    "Anthony AI the Supreme": "Anthony AI the Supreme",
    "Anthony AI the Supreme": "Anthony AI the Supreme",
    "Anthony AI the Supreme": "Anthony AI the Supreme",
    "Anthony AI the Supreme": "Anthony AI the Supreme",
    "Anthony AI the Supreme": "Anthony AI the Supreme",
    "anthony_ai_supreme": "anthony_ai_supreme",
    "🦾": "🦾" # Changing robot to more 'bad ass' mechanical arm/mascot
}

def rebrand():
    # Process Root, app/src/main/assets, and obsidian_edge_root
    dirs = [root, root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root", root / "colony_backend", root / "assets"]

    for d in dirs:
        if not d.exists(): continue
        print(f"[*] Rebranding in: {d}")
        for file_path in d.rglob("*"):
            if file_path.is_dir(): continue
            if ".git" in str(file_path) or "venv" in str(file_path) or "__pycache__" in str(file_path): continue
            if file_path.suffix not in [".html", ".js", ".py", ".css", ".kt"]: continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                modified = False
                for old, new in mappings.items():
                    if old in content:
                        # Case sensitive for names
                        content = content.replace(old, new)
                        modified = True

                if modified:
                    file_path.write_text(content, encoding="utf-8")
                    print(f"✓ Rebranded: {file_path.relative_to(root)}")
            except Exception as e:
                print(f"[-] Error processing {file_path}: {e}")

if __name__ == "__main__":
    rebrand()
