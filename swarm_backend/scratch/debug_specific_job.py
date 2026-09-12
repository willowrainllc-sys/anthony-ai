import os

def debug(job_id):
    log_path = r'D:\ObsidianAi_Swarm\Logs\empire_master.log'
    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()

    print(f"--- LOGS FOR {job_id} ---")
    for line in lines:
        if job_id in line:
            print(line.strip())

if __name__ == "__main__":
    debug("job_15m_26a72f")
