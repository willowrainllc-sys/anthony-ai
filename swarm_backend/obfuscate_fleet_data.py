import os
import re
from pathlib import Path

PORTAL_DIR = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\willow_rain_global\wholesale_portal")

# Patterns to obfuscate the secret fleet size and name
REPLACEMENTS = [
    (r"103[ -]node", "Sovereign-grade"),
    (r"5,103[ -]node", "Industrial-grade"),
    (r"5103[ -]node", "Industrial-grade"),
    (r"103[ -]MUSTANGS", "GRID_SECURED"),
    (r"103[ -]Mustangs", "GRID_SECURED"),
    (r"5,103[ -]NODES", "DECENTRALIZED_GRID"),
    (r"5103[ -]NODES", "DECENTRALIZED_GRID"),
    (r"103[ -]ASI Nodes", "Sovereign Intelligence Nodes"),
    (r"103[ -]root blades", "Sovereign root blades"),
    (r"103[ -]Humanoid ASI Nodes", "Sovereign Intelligence Mesh"),
    (r"103[ -]Mustang Nodes", "Secure Grid Nodes"),
    (r"103[ -]Mustang Cluster", "Secure Grid Cluster"),
    (r"103[ -]phones", "Secure Nodes"),
    (r"103[ -]phone", "Secure Node"),
    (r"103[ -]Mustangs", "Secure Nodes"),
    (r"Mustang", "Node")
]

def obfuscate():
    files = list(PORTAL_DIR.glob("*.html")) + list(PORTAL_DIR.glob("*.js")) + list(PORTAL_DIR.glob("*.json"))

    for file_path in files:
        if file_path.name == "aiphony_manifest.json": continue # Keep internal data intact

        content = file_path.read_text(encoding='utf-8', errors='ignore')
        new_content = content

        for pattern, replacement in REPLACEMENTS:
            new_content = re.sub(pattern, replacement, new_content, flags=re.IGNORECASE)

        if content != new_content:
            file_path.write_text(new_content, encoding='utf-8')
            print(f"✓ Obfuscated: {file_path.name}")

if __name__ == "__main__":
    obfuscate()
