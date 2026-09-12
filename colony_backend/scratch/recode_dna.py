import os
from pathlib import Path

# Paths to process
DIRS = [
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\colony_backend"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\ingress_api"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\willow_rain_global\cellular_stack")
]

REPLACEMENTS = {
    "sovereign": "obsidian",
    "Sovereign": "Obsidian",
    "supreme": "obsidian",
    "Supreme": "Obsidian"
}

def recode_dna():
    print("=== 🪐 OBSIDIAN DNA RECODE: REMOVING LEGACY TRACES ===\n")
    update_count = 0

    for d in DIRS:
        if not d.exists(): continue
        for f in d.glob("*.py"):
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                new_content = content
                for old, new in REPLACEMENTS.items():
                    new_content = new_content.replace(old, new)

                if new_content != content:
                    f.write_text(new_content, encoding='utf-8')
                    print(f"  [✓] UPDATED DNA: {f.name}")
                    update_count += 1
            except Exception as e:
                print(f"  [-] ERROR {f.name}: {e}")

    print(f"\n🪐 DNA RECODE COMPLETE: {update_count} files transitioned to OBSIDIAN.")

if __name__ == "__main__":
    recode_dna()
