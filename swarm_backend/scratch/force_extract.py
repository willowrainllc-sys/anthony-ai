import asyncio
import sys
import os
import json
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from sovereign_quant_engine import quant_engine

async def force():
    print('=== 🔱 SUPREME DIRECTIVE: FORCING REAL-WORLD VALUE EXCTRACTION ===\n')

    print('[1/2] QUANT ENGINE: Extracting value from Robinhood...')
    res = await quant_engine.execute_algorithmic_scalp()
    print(f"      STATUS: {res.get('status')}")

    print('\n[2/2] VAULT EXTRACTION: Scanning for locked Gift Cards...')
    conn = sqlite3.connect(r'C:\ObsidianAi_Swarm\Empire_Vault.db')
    rows = conn.execute("SELECT card_type, card_code, value_usd FROM gift_card_vault WHERE status='READY_TO_REDEEM'").fetchall()

    if rows:
        print(f'      [✓] FOUND {len(rows)} REAL GIFT CARDS READY TO USE NOW:')
        for r in rows:
            print(f"          - {r[0]} | ${r[2]:.2f} | CODE: {r[1]}")
    else:
        print('      [!] VAULT EMPTY: Disciples are still playing.')
        print('      -> To get cash THIS SECOND, log into obsidian.global.holdings@gmail.com and check the "Updates" or "Promotions" folder for InboxDollars/Freecash emails.')

    conn.close()

if __name__ == "__main__":
    asyncio.run(force())
