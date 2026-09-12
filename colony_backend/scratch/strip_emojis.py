import os
from pathlib import Path

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\colony_backend")

def strip_emojis():
    print("=== 🔱 OBSIDIAN LOG STRIP: REMOVING NON-ASCII CHARACTERS ===\n")
    for f in ROOT.glob("*.py"):
        try:
            content = f.read_text(encoding='utf-8', errors='ignore')
            # Replace common emojis with text or remove
            new_content = content.replace("🔱", "[SUPREME]").replace("🪐", "[SATURN]").replace("⚛️", "[ATOMIC]")
            new_content = new_content.replace("⚠️", "[ALERT]").replace("💀", "[DEATH]").replace("✅", "[SUCCESS]")
            new_content = new_content.replace("🚀", "[STRIKE]").replace("💰", "[CASH]").replace("💸", "[WEALTH]")
            new_content = new_content.replace("📊", "[DATA]").replace("📡", "[SIGNAL]").replace("🕵️‍♂️", "[SHADOW]")
            new_content = new_content.replace("🧠", "[BRAIN]").replace("🏛️", "[IMPERIUM]").replace("🔌", "[LINK]")
            new_content = new_content.replace("💎", "[OBSIDIAN]")

            # Remove any remaining non-ascii characters
            new_content = new_content.encode("ascii", "ignore").decode("ascii")

            if new_content != content:
                f.write_text(new_content)
                print(f"  [✓] CLEANED: {f.name}")
        except: pass

if __name__ == "__main__":
    strip_emojis()
