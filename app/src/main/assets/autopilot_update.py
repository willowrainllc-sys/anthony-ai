# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- OBSIDIAN CITY AUTOPILOT UPDATE ENGINE v1.0 ---
import os
import time
import subprocess

def sync_updates():
    print("[*] Checking GitHub for new digital assets...")
    try:
        # Force pull from master
        subprocess.run(["git", "fetch", "origin"], check=True)
        result = subprocess.run(["git", "pull", "origin", "master"], capture_output=True, text=True)

        if "Already up to date" not in result.stdout:
            print("🔱 NEW UPDATE DETECTED. Syncing platform...")
            print(result.stdout)
            # You can add a command here to restart the server if needed
        else:
            print("● System current. No new ingress.")

    except Exception as e:
        print(f"[-] Sync Error: {e}")

if __name__ == "__main__":
    print("🔱 AUTOPILOT UPDATE ENGINE ACTIVE")
    while True:
        sync_updates()
        time.sleep(30) # Check every 30 seconds
