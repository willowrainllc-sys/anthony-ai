import os

def debug():
    log_path = r'D:\ObsidianAi_Swarm\Logs\empire_master.log'
    if not os.path.exists(log_path):
        print("Log not found")
        return

    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    print("--- SEARCHING FOR RENDER ERRORS ---")
    count = 0
    for line in reversed(lines):
        if any(k in line for k in ['OPENCUT', 'WORKER', 'FATAL', 'ERROR']):
            print(line.strip())
            count += 1
            if count > 50:
                break

if __name__ == "__main__":
    debug()
