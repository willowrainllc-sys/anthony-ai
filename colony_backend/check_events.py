import sqlite3
try:
    conn = sqlite3.connect('C:/AnthonyAi_Colony/Empire_Vault.db')
    rows = conn.execute('SELECT event_type, metadata, timestamp FROM empire_events ORDER BY timestamp DESC LIMIT 20').fetchall()
    for r in rows:
        print(f"[{r[2]}] {r[0]}: {r[1]}")
    conn.close()
except Exception as e:
    print(f"Error: {e}")
