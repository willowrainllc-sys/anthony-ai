# --- WILLOW RAIN COMPANY LLC: OBSIDIAN TREASURY & ALLOCATION MANAGER v1.0 ---
import os
import json
import uuid
import time
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from pathlib import Path

from colony_logger import colony_log
from colony_persistence import db

# ALLOCATION RULES (Total 100%)
TAX_RESERVE_PCT = 0.25      # 25% for Corporate Taxes
TEAM_PAYOUT_PCT = 0.30      # 30% for Partners/Disciples
OPERATIONS_PCT = 0.15       # 15% for Reinvestment/Servers
DIRECTOR_DRAW_PCT = 0.30     # 30% for Obsidian Christopher Maestas

class TreasuryBucket(BaseModel):
    name: str
    allocated_usd: float = 0.0
    description: str

class ObsidianTreasuryManager:
    """
    OBSIDIAN TREASURY MANAGER v1.0:
    Ensures money is 'Managed and Split Right'.
    1. REVENUE SPLITTING: Breaks down every incoming dollar into protected buckets.
    2. TAX COMPLIANCE: Automatically sets aside 25% for end-of-year settlement.
    3. TEAM DISTRIBUTION: Manages the 30% 'Colony' commission pool.
    4. DIRECTOR SETTLEMENT: Prepares the final 30% net draw for Obsidian.
    """
    def __init__(self):
        self._init_treasury_vault()

    def _init_treasury_vault(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS treasury_ledger (
                    bucket_name TEXT PRIMARY KEY,
                    balance_usd REAL,
                    last_update REAL
                )
            """)
            # Initialize buckets if they don't exist
            buckets = [
                ("TAX_RESERVE", "For end-of-year corporate tax liability."),
                ("TEAM_PAYOUTS", "Commissions for sister partners and disciples."),
                ("OPERATIONS", "Server costs, API keys, and capital flips."),
                ("DIRECTOR_DRAW", "Net profit for Obsidian Christopher Maestas.")
            ]
            for name, desc in buckets:
                conn.execute("INSERT OR IGNORE INTO treasury_ledger (bucket_name, balance_usd, last_update) VALUES (?, ?, ?)",
                             (name, 0.0, time.time()))
            conn.commit()

    async def allocate_incoming_revenue(self, amount_usd: float, source: str = "GENERAL"):
        """Splits incoming revenue into the obsidian buckets."""
        colony_log(f"TREASURY: Allocating ${amount_usd:,.2f} from [{source}]...", node="TREASURY")

        splits = {
            "TAX_RESERVE": amount_usd * TAX_RESERVE_PCT,
            "TEAM_PAYOUTS": amount_usd * TEAM_PAYOUT_PCT,
            "OPERATIONS": amount_usd * OPERATIONS_PCT,
            "DIRECTOR_DRAW": amount_usd * DIRECTOR_DRAW_PCT
        }

        with db._get_connection() as conn:
            for bucket, val in splits.items():
                conn.execute("UPDATE treasury_ledger SET balance_usd = balance_usd + ?, last_update = ? WHERE bucket_name = ?",
                             (val, time.time(), bucket))
            conn.commit()

        colony_log(f" TREASURY SUCCESS: Revenue split complete. Director Draw: +${splits['DIRECTOR_DRAW']:,.2f}", node="TREASURY")

        db.log_event("TREASURY", "REVENUE_ALLOCATED", {
            "source": source,
            "total": amount_usd,
            "director_share": splits["DIRECTOR_DRAW"]
        })

        return splits

    def get_treasury_status(self) -> List[Dict[str, Any]]:
        """Returns the current state of all treasury buckets."""
        with db._get_connection() as conn:
            rows = conn.execute("SELECT bucket_name, balance_usd FROM treasury_ledger").fetchall()

        return [{"bucket": r[0], "balance": round(r[1], 2)} for r in rows]

treasury_manager = ObsidianTreasuryManager()

if __name__ == "__main__":
    import asyncio
    async def test_treasury():
        # Simulate a $5,000 day
        await treasury_manager.allocate_incoming_revenue(5000.00, source="B2B_Wholesale_Contract")
        status = treasury_manager.get_treasury_status()
        print("\n=== [SUPREME] WILLOW RAIN TREASURY LEDGER ===")
        for b in status:
            print(f"- {b['bucket']}: ${b['balance']:,.2f}")

    asyncio.run(test_treasury())
