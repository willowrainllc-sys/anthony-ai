import os
import asyncio
import httpx
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Absolute Path Correction
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
sys_path = str(ROOT / "swarm_backend")
import sys
sys.path.append(sys_path)
load_dotenv(ROOT / ".env")

TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
LOC_ID = "L1H0AHZQR8T4G" # willow rain Co
DB_PATH = r'C:\AnthonyAi_Swarm\Empire_Vault.db'

async def physical_truth_audit():
    print("=== 🔱 OBSIDIAN PRODUCTION AUDIT: NO LIES ===")

    headers = {
        "Square-Version": "2024-10-17",
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 1. Audit Square Invoices
        print("[*] Auditing Square Settlements...")
        resp = await client.get(f"https://connect.squareup.com/v2/invoices?location_id={LOC_ID}", headers=headers)
        if resp.status_code == 200:
            invoices = resp.json().get('invoices', [])
            negotiating_total = 0
            for inv in invoices:
                if inv['status'] in ['UNPAID', 'PARTIALLY_PAID']:
                    amount = inv['payment_requests'][0].get('computed_amount_money', {}).get('amount', 0) / 100
                    negotiating_total += amount
                    print(f"  [NEGOTIATING] {inv['title']} | ${amount:,.2f}")
            print(f"✓ TOTAL NEGOTIATING: ${negotiating_total:,.2f}")
        else:
            print(f"[-] SQUARE ERROR: {resp.status_code}")

    # 2. Audit Video Swarm
    print("\n[*] Auditing Social Hub Ingress...")
    conn = sqlite3.connect(DB_PATH)
    try:
        # Check if the title column is really there
        cursor = conn.execute("PRAGMA table_info(production_jobs)")
        cols = [c[1] for c in cursor.fetchall()]
        print(f"  [SCHEMA] production_jobs columns: {cols}")

        # Check for READY videos
        ready_count = conn.execute("SELECT COUNT(*) FROM production_jobs WHERE status='READY'").fetchone()[0]
        print(f"  [CONTENT] Videos ready for push: {ready_count}")

        # Check for FAILED social tasks
        failed = conn.execute("SELECT channel, error_log FROM swarm_tasks WHERE status='FAILED' LIMIT 3").fetchall()
        for f in failed:
            print(f"  [ERROR] {f[0]}: {f[1]}")
    finally:
        conn.close()

if __name__ == "__main__":
    asyncio.run(physical_truth_audit())
