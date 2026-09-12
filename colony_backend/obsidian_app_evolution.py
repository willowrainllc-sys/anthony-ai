import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\app")

REPLACEMENTS = [
    (r"swarm", "colony"),
    (r"Swarm", "Colony"),
    (r"SWARM", "COLONY"),
    (r"strike", "burst"),
    (r"Strike", "Burst"),
    (r"STRIKE", "BURST"),
    (r"103 Nodes", "The Nest"),
    (r"103 nodes", "The Nest"),
    (r"103-node", "Nest-node"),
    (r"103 Node", "The Nest"),
    (r"103 Mustang Nodes", "103 Oracles of the Nest"),
    (r"103 independent clones", "103 Oracles"),
    (r"103-phone", "Nest-phone")
]

def evolve_app():
    extensions = [".kt", ".xml", ".gradle", ".kts"]

    for file_path in ROOT.rglob("*"):
        if file_path.suffix in extensions:
            try:
                content = file_path.read_text(encoding='utf-8', errors='ignore')
                new_content = content
                for pattern, replacement in REPLACEMENTS:
                    new_content = re.sub(pattern, replacement, new_content)

                if content != new_content:
                    file_path.write_text(new_content, encoding='utf-8')
                    print(f"✓ App Evolved: {file_path.relative_to(ROOT)}")
            except Exception as e:
                print(f"[-] Error in {file_path}: {e}")

if __name__ == "__main__":
    evolve_app()
