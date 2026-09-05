import os
import glob
from pathlib import Path

def purge_broll():
    print("=== PURGING ALL CACHED B-ROLL & STOCK FOOTAGE ===")
    dirs = [
        Path(r"D:\AnthonyAi_Swarm\Secure_Assets\source_videos"),
        Path(r"D:\AnthonyAi_Swarm\Secure_Assets\local_broll_library"),
        Path(r"D:\AnthonyAi_Swarm\Renderings"),
        Path(r"C:\AnthonyAi_Swarm\Renderings")
    ]
    total_removed = 0
    for d in dirs:
        if d.exists():
            files = list(d.glob("*.mp4"))
            for f in files:
                try:
                    os.remove(f)
                    total_removed += 1
                except Exception as e:
                    print(f"Error deleting {f}: {e}")
            print(f"Purged {len(files)} mp4 files from {d}")
    print(f"SUCCESS: Total {total_removed} old video files purged.")

if __name__ == "__main__":
    purge_broll()
