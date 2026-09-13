# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- EMPIRE JARGON PURGE v1.0 ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# Mappings for Professional Rebranding
mappings = {
    "AI Business Assistant": "AI Business Assistant",
    "business growth": "business growth",
    "business growth": "business growth",
    "Enterprise AI Node": "Enterprise AI Node",
    "High-Performance": "High-Performance",
    "high-performance": "high-performance",
    "Advanced": "Advanced",
    "Director Dashboard": "Director Dashboard",
    "Business Starter Bundle": "Business Starter Bundle",
    "Management Console": "Management Console",
    "System Access": "System Access",
    "system access": "system access",
    "Global Edge Network": "Global Edge Network",
    "global edge network": "global edge network",
    "Operational status": "Operational status",
    "operational status": "operational status",
    "System Administrator": "System Administrator",
    "Enterprise AI": "Enterprise AI",
    "enterprise AI": "enterprise AI",
    "Business Infrastructure": "Business Infrastructure",
    "Digital Business": "Digital Business",
    "digital business": "digital business",
    "Wholesale Access": "Wholesale Access"
}

def purge_jargon():
    # Process Root, app/src/main/assets, and obsidian_edge_root
    dirs = [root, root / "app" / "src" / "main" / "assets", root / "obsidian_edge_root", root / "colony_backend", root / "assets"]

    for d in dirs:
        if not d.exists(): continue
        print(f"[*] Purging Jargon in: {d}")
        for file_path in d.rglob("*"):
            if file_path.is_dir(): continue
            if ".git" in str(file_path) or "venv" in str(file_path) or "__pycache__" in str(file_path): continue
            if file_path.suffix not in [".html", ".js", ".py", ".css", ".kt"]: continue

            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                modified = False
                for old, new in mappings.items():
                    if old in content:
                        content = content.replace(old, new)
                        modified = True

                if modified:
                    file_path.write_text(content, encoding="utf-8")
                    print(f"✓ Rebranded: {file_path.relative_to(root)}")
            except Exception as e:
                print(f"[-] Error processing {file_path}: {e}")

if __name__ == "__main__":
    purge_jargon()
