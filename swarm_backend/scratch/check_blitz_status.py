import sqlite3

def check():
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    # Use simple SELECT COUNT(*)
    row = conn.execute("SELECT COUNT(*) FROM empire_events WHERE event_type='ACCOUNT_FACTORY_SUCCESS'").fetchone()
    print(f"SUPREME_ACCOUNTS_CREATED: {row[0]}")
    conn.close()

if __name__ == "__main__":
    check()
