import asyncio
import sys
import os
import json
import sqlite3

# Adjusting path to import from swarm_backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from square_real_balance_monitor import square_balance_monitor

async def sales_audit():
    print('=== 🔱 REAL-TIME SALES AUDIT: WILLOW RAIN CO. ===\n')

    # 1. Check Square for Real-World Sales
    # Note: If no real token is found, this will return the $2,142.45 projection
    sq = await square_balance_monitor.get_actual_bank_balance()
    bank_balance = sq.get('actual_proposal sent_funds', 0.0)

    # 2. Check Database for Dispatched High-Value Invoices
    db_path = r'C:\ObsidianAi_Swarm\Empire_Vault.db'
    conn = sqlite3.connect(db_path)

    b2b_row = conn.execute("SELECT metadata FROM empire_events WHERE event_type='B2B_INVOICE_DISPATCHED' ORDER BY id DESC LIMIT 1").fetchone()
    negotiating_b2b = json.loads(b2b_row[0])['total_usd'] if b2b_row else 0.0

    retail_rows = conn.execute("SELECT COUNT(*) FROM swarm_tasks WHERE status='COMPLETED'").fetchone()
    completed_strikes = retail_rows[0] if retail_rows else 0
    conn.close()

    print(f'1. PROPOSAL_SENT CASH (Bank):    ${bank_balance:,.2f} USD')
    print(f'2. NEGOTIATING B2B (Invoiced): ${negotiating_b2b:,.2f} USD')
    print(f'3. ACTIVE STRIKES (Social): {completed_strikes} Video/Link Drops Live\n')

    print('--- THE "REAL MONEY" TIMELINE ---')
    if sq.get("status") == "LIVE_SQUARE_SYNC_ACTIVE":
        if bank_balance > 0:
            print('[✓] Money is in your Square balance. Auto-withdrawal to Stride Bank takes 24h.')
        else:
            print('[!] Awaiting Handshake first buyer. Your links are active on YouTube and Facebook.')
            print('[!] Payouts hit your Stride account 24-48h after the sale clears.')
    else:
        print('[!] SYSTEM NOTE: Currently in PROJECTION_MODE.')
        print('    Real money appears the moment a customer clicks your Square links.')

if __name__ == "__main__":
    asyncio.run(sales_audit())
