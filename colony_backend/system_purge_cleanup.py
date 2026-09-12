# --- WILLOW RAIN SECURITY: SYSTEM PURGE & REDUNDANCY CLEANUP v2.0 ---
import os
import shutil
from pathlib import Path

# TARGETS FOR DELETION (Legacy / Redundant / Broken)
JUNK_SCRIPTS = [
    "bradautomates_claude_video.py",
    "claude_video_engine.py",
    "ltx_pipelines.py",
    "repair_ltx_model.py",
    "theme_engine.py",
    "populate_store.py",
    "wipe_store.py",
    "store_sales_burstr.py",
    "viking_context_engine.py",
    "viking_context_engine.py",
    "demonstrate_team_chat.py",
    "manual_amigos_burst.py",
    "manual_feed_burst.py",
    "manual_frontend_trigger.py",
    "interactive_game_login.py",
    "game_rewards_browser_bot.py",
    "lottery_data_bot.py",
    "usb_bootstrapper.py"
]

TEMP_FOLDERS = [
    Path(r"D:\ObsidianAi_Colony\Secure_Assets\renderings"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\app\build"),
    Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\.gradle")
]

def execute_obsidian_purge():
    print("=== [SUPREME] SUPREME SYSTEM PURGE: WILLOW RAIN SECURITY ===\n")

    # 1. Purge Junk Scripts
    backend_dir = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\colony_backend")
    purged_count = 0
    for script in JUNK_SCRIPTS:
        spath = backend_dir / script
        if spath.exists():
            try:
                os.remove(spath)
                print(f"[] PURGED: {script}")
                purged_count += 1
            except: pass

    # 2. Purge Temp Data & Caches
    for folder in TEMP_FOLDERS:
        if folder.exists():
            try:
                shutil.rmtree(folder)
                folder.mkdir(parents=True, exist_ok=True)
                print(f"[] CLEANED: {folder}")
            except: pass

    # 3. Purge Large Log Files
    logs_dir = Path(r"D:\ObsidianAi_Colony\Logs")
    if logs_dir.exists():
        for f in logs_dir.glob("*.log"):
            if f.stat().st_size > 10 * 1024 * 1024: # 10MB
                os.remove(f)
                print(f"[] PURGED LARGE LOG: {f.name}")

    print(f"\n[SUPREME] PURGE COMPLETE: {purged_count} legacy scripts removed. System is lean.")

if __name__ == "__main__":
    execute_obsidian_purge()
