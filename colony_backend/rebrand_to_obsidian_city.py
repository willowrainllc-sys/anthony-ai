# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- REVERT REBRAND: ANTHONY AI -> OBSIDIAN AI v1.0 ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# Mappings for Reverting to Obsidian City / Obsidian AI
mappings = {
    "Anthony AI the Supreme Builder": "Obsidian AI Builder",
    "Anthony AI the Supreme AI": "Obsidian AI",
    "Anthony AI the Supreme Engine": "Obsidian AI Engine",
    "Anthony AI the Supreme": "Obsidian AI",
    "anthony_ai_supreme": "obsidian_ai",
    "Greetings. I am Anthony AI, your Supreme Sovereign Oracle.": "Greetings. I am Obsidian AI, your AI business assistant.",
    "🦾": "🤖", # Reverting icon to robot
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?q=80&w=200&h=200&auto=format&fit=crop": "https://images.unsplash.com/photo-1614728263952-84ea256f9679?q=80&w=100&h=100&auto=format&fit=crop", # Reverting Godfather image to AI mascot
    "obsidian_anthony_ai_supreme_builder.html": "obsidian_leo_builder.html"
}

def revert_rebrand():
    # Target frontend directories
    dirs = [root, root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root", root / "assets"]

    for d in dirs:
        if not d.exists(): continue
        print(f"[*] Reverting to Obsidian Branding in: {d}")
        for file_path in d.rglob("*"):
            if file_path.is_dir(): continue
            if ".git" in str(file_path) or "venv" in str(file_path) or "__pycache__" in str(file_path): continue
            if file_path.suffix not in [".html", ".js", ".css"]: continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                modified = False
                for old, new in mappings.items():
                    if old in content:
                        content = content.replace(old, new)
                        modified = True

                if modified:
                    file_path.write_text(content, encoding="utf-8")
                    print(f"[+] Reverted: {file_path.relative_to(root)}")
            except Exception as e:
                print(f"[-] Error processing {file_path}: {e}")

if __name__ == "__main__":
    revert_rebrand()
