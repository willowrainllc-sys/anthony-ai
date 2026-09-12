import time
import os

log_path = r'D:\ObsidianAi_Swarm\Logs\empire_master.log'

def tail_forever():
    print("=== 🔱 WILLOW RAIN SECURITY: MASTER TERMINAL LIVE FEED ===\n")
    if not os.path.exists(log_path):
        print(f"Waiting for log file at {log_path}...")
        while not os.path.exists(log_path):
            time.sleep(1)

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        # Go to the end of the file
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.5)
                continue
            print(line.strip())

if __name__ == "__main__":
    try:
        tail_forever()
    except KeyboardInterrupt:
        print("\nTerminal Closed.")
