import sqlite3
import json

def check():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    row = conn.execute('SELECT manifest FROM production_jobs WHERE job_id="job_15m_c0818b"').fetchone()
    if row:
        m = json.loads(row[0])
        print("TITLE:", m.get('title'))
        print("SCENES COUNT:", len(m.get('scenes', [])))
        for i, s in enumerate(m.get('scenes', [])):
            print(f"  Scene {i+1}: path={s.get('path')} (Exists: {os.path.exists(s.get('path')) if s.get('path') else False})")
    else:
        print("Job not found")
    conn.close()

import os
if __name__ == "__main__":
    check()
