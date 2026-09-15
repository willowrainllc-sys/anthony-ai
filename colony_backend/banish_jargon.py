# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- EMPIRE BRAND HARDENING v2.0 (PRODUCTION) ---
import os
from pathlib import Path

root = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")

# Mappings for Professional/Enterprise Rebranding
mappings = {
    "High-Aura": "High-Performance",
    "high-aura": "high-performance",
    "Elite": "Professional",
    "elite": "professional",
    "Strike": "Campaign",
    "strike": "campaign",
    "Handshake": "Integration",
    "handshake": "integration",
    "Sovereign": "Independent",
    "sovereign": "independent",
    "Disciple": "Associate",
    "disciple": "associate",
    "Colony": "Network",
    "colony": "network",
    "Aura": "Performance",
    "aura": "performance"
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
                    print(f"[+] Rebranded: {file_path.relative_to(root)}")
            except Exception as e:
                print(f"[-] Error processing {file_path}: {e}")

if __name__ == "__main__":
    purge_jargon()