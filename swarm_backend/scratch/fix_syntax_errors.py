import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_backend")

def fix_syntax():
    print("=== 🪐 OBSIDIAN SYNTAX REPAIR: FIXING BRAIN BUGS ===\n")

    # 1. Fix obsidian_obsidian_bridge_autoclaim.py
    f1 = ROOT / "obsidian_obsidian_bridge_autoclaim.py"
    if f1.exists():
        content = f1.read_text()
        new_content = content.replace("class Obsidian BridgeAutoClaimEngine:", "class ObsidianBridgeAutoClaimEngine:")
        f1.write_text(new_content)
        print(f"  [✓] FIXED: {f1.name}")

    # 2. Fix anthony_persistence_engine.py
    f2 = ROOT / "anthony_persistence_engine.py"
    if f2.exists():
        content = f2.read_text()
        new_content = content.replace("class Anthony ChristopherPersistenceEngine:", "class AnthonyChristopherPersistenceEngine:")
        f2.write_text(new_content)
        print(f"  [✓] FIXED: {f2.name}")

    # 3. Fix anthony_command_os.py (class name spaces)
    f3 = ROOT / "anthony_command_os.py"
    if f3.exists():
        content = f3.read_text()
        new_content = content.replace("class Anthony ChristopherCommandOS:", "class AnthonyChristopherCommandOS:")
        new_content = new_content.replace("from anthony_ingress_engine import Anthony ChristopherIngressEngine", "from anthony_ingress_engine import AnthonyChristopherIngressEngine")
        new_content = new_content.replace("engine = Anthony ChristopherIngressEngine", "engine = AnthonyChristopherIngressEngine")
        new_content = new_content.replace("grid_os = Anthony ChristopherCommandOS()", "grid_os = AnthonyChristopherCommandOS()")
        f3.write_text(new_content)
        print(f"  [✓] FIXED: {f3.name}")

if __name__ == "__main__":
    fix_syntax()
