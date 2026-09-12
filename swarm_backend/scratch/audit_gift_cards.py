import sqlite3
import os

def audit():
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    if not os.path.exists(db_path):
        print("Database not found")
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("\n=== 🔱 WILLOW RAIN GIFT CARD VAULT ===\n")
    rows = cur.execute("SELECT card_type, card_code, value_usd, status FROM gift_card_vault").fetchall()

    if not rows:
        print("No gift card codes found in vault yet.")
        print("Reason: Swarm Disciples are currently running game/survey exploits. Extracts appear in Gmail unread.")
    else:
        for r in rows:
            print(f"- {r[0]} | Value: ${r[2]:.2f} | Status: {r[3]}")
            print(f"  CODE: {r[1]}")

    conn.close()

if __name__ == "__main__":
    audit()
