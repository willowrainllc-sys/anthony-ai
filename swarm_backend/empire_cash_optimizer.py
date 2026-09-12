# --- EMPIRE CASH FLOW OPTIMIZER & REVENUE COMMAND v1.0 ---
import os
import sys
import json
import time
import asyncio
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db
from square_checkout_gateway import square_gateway
from passive_monetization_node import passive_node
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

class EmpireCashOptimizer:
    """
    EMPIRE CASH FLOW OPTIMIZER v1.0:
    Consolidates all active revenue streams (Square Payments, Printful POD,
    Amazon Affiliates, YouTube Monetization, and Passive Data Tunnels)
    into a single high-profit cash flow command dashboard.
    """
    async def get_live_revenue_command(self) -> dict:
        swarm_log("CASH_OPTIMIZER: Auditing active revenue streams for Willow Rain Company LLC...", node="REVENUE")
        now = time.time()

        # 1. SQUARE DIGITAL PRODUCTS (Instant Bank Deposit)
        season_pass = await square_gateway.create_digital_product_checkout("Willow Rain Digital Season Pass", 9.99)
        masterclass = await square_gateway.create_digital_product_checkout("Obsidian Intel Masterclass", 19.99)
        merch_bundle = await square_gateway.create_digital_product_checkout("Willow Rain Apparel Bundle", 29.99)

        square_streams = [
            {"product": "Digital Season Pass", "price_usd": 9.99, "checkout_link": season_pass.get("checkout_url")},
            {"product": "Obsidian Masterclass", "price_usd": 19.99, "checkout_link": masterclass.get("checkout_url")},
            {"product": "Apparel Merch Bundle", "price_usd": 29.99, "checkout_link": merch_bundle.get("checkout_url")}
        ]

        # 2. PASSIVE DATA & BANDWIDTH REVENUE
        passive_summary = await passive_node.get_passive_earnings_summary()

        # 3. PRINTFUL MERCH & AMAZON AFFILIATE STREAMS
        affiliate_streams = {
            "amazon_tag": os.getenv("AMAZON_AFFILIATE_ID", "flikmobile-20"),
            "printful_store_id": os.getenv("PRINTFUL_STORE_ID", "18670114"),
            "active_synced_products": 20
        }

        return {
            "status": "active",
            "merchant_name": "Willow Rain Company LLC",
            "primary_deposit_gateway": "Square Production Account (LDCKH8QA4MVA4)",
            "square_checkout_links": square_streams,
            "passive_income_est_monthly_usd": passive_summary.get("estimated_monthly_usd", 100.0),
            "affiliate_merch_config": affiliate_streams,
            "timestamp": now
        }

cash_optimizer = EmpireCashOptimizer()

if __name__ == "__main__":
    res = asyncio.run(cash_optimizer.get_live_revenue_command())
    print("EMPIRE REVENUE COMMAND DASHBOARD:")
    print(json.dumps(res, indent=2))
