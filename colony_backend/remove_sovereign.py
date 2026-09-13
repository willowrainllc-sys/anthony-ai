# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- REMOVE SOVEREIGN FROM FRONTEND v1.0 ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# Mappings for professional removal of 'Sovereign'
mappings = {
    "Sovereign AI Oracle": "AI Business Assistant",
    "Sovereign AI": "Enterprise AI",
    "sovereign AI": "enterprise AI",
    "Sovereign Link Active": "Link Active",
    "Sovereign Infrastructure": "Business Infrastructure",
    "Sovereign Cloud & Identity": "Cloud & Identity Hub",
    "Sovereign Cloud Mesh": "Global Edge Mesh",
    "Sovereign Data": "Private Data",
    "Stay sovereign": "Stay independent",
    "stay sovereign": "stay independent",
    "Sovereign": "Private", # Generic fallback
    "sovereign": "private", # Generic fallback
}

def remove_sovereign():
    # Targets: HTML, JS, CSS in root and asset folders
    dirs = [root, root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root", root / "assets"]

    for d in dirs:
        if not d.exists(): continue
        print(f"[*] Removing 'Sovereign' from: {d}")
        for file_path in d.rglob("*"):
            if file_path.is_dir(): continue
            if ".git" in str(file_path) or "venv" in str(file_path) or "__pycache__" in str(file_path): continue
            if file_path.suffix not in [".html", ".js", ".css"]: continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                original_content = content

                # Special case for the hero quotes in index.html to ensure they look good
                if file_path.name == "index.html":
                    content = content.replace('Build your sovereign brand.', 'Build your global brand.')

                for old, new in mappings.items():
                    if old in content:
                        content = content.replace(old, new)

                if content != original_content:
                    file_path.write_text(content, encoding="utf-8")
                    print(f"✓ Cleaned: {file_path.relative_to(root)}")
            except Exception as e:
                print(f"[-] Error processing {file_path}: {e}")

if __name__ == "__main__":
    remove_sovereign()
