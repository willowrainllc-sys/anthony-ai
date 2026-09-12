import sqlite3
import os

def fix():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    conn.execute("UPDATE swarm_tasks SET status='NEGOTIATING' WHERE id=591")
    conn.commit()
    print("Task 591 reset.")
    conn.close()

if __name__ == "__main__":
    fix()
