import os
import re
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\colony_backend")

def fix_all():
    print("=== 🔱 FINAL ENGINE ALIGNMENT: FIXING ALL BUGS ===\n")

    # 1. Fix obsidian_ingress_data_flow_auditor.py
    f1 = ROOT / "obsidian_ingress_data_flow_auditor.py"
    if f1.exists():
        content = f1.read_text(encoding='utf-8')
        new_content = content.replace("class Obsidian IngressDataFlowAuditor:", "class ObsidianIngressDataFlowAuditor:")
        f1.write_text(new_content, encoding='utf-8')
        print(f"  [✓] FIXED SYNTAX: {f1.name}")

    # 2. Fix daemon_worker.py imports
    f2 = ROOT / "daemon_worker.py"
    if f2.exists():
        content = f2.read_text(encoding='utf-8')
        new_content = content.replace("from obsidian_persistence_engine", "from anthony_persistence_engine")
        new_content = new_content.replace("import obsidian_persistence_engine", "import anthony_persistence_engine")
        f2.write_text(new_content, encoding='utf-8')
        print(f"  [✓] FIXED IMPORTS: {f2.name}")

    # 3. Mass repair for any other space-character class bugs
    for f in ROOT.glob("*.py"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            # Look for 'class Name Name:'
            new_content = re.sub(r'class\s+Obsidian\s+(\w+):', r'class Obsidian\1:', content)
            new_content = re.sub(r'class\s+Anthony\s+Christopher(\w+):', r'class AnthonyChristopher\1:', content)
            if new_content != content:
                f.write_text(new_content, encoding='utf-8')
                print(f"  [✓] AUTO-REPAIRED CLASS: {f.name}")
        except: pass

if __name__ == "__main__":
    fix_all()
