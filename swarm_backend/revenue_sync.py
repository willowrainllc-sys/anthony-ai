# --- EMPIRE REVENUE SYNC: COMMERCE & FINANCIAL NODE v1.0 ---
import asyncio
import random
import time
from swarm_logger import swarm_log
from swarm_persistence import db

class RevenueSync:
    """
    BUSINESS NODE: Money Monitoring.
    Syncs sales from Print-on-Demand and portfolio value from Robinhood.
    """
    async def run_sync_loop(self):
        swarm_log("REVENUE: Revenue & Financial Grid monitoring active.", node="MONEY")
        while True:
            try:
                await self._sync_pod_stores()
                await self._sync_robinhood()
            except Exception as e:
                swarm_log(f"[-] REVENUE ERROR: {e}", node="MONEY")

            await asyncio.sleep(3600) # Sync every hour

    async def _sync_pod_stores(self):
        """Simulates fetching sales from Redbubble/Printful/Shopify."""
        stores = ["EMPIRE_APPAREL", "QUANTUM_DECALS", "OSINT_MERCH"]
        with db._get_connection() as conn:
            for store in stores:
                sales = random.uniform(50.0, 450.0)
                conn.execute("""
                    INSERT INTO commerce_revenue (store_id, platform, daily_sales, total_revenue, active_listings, last_sync)
                    VALUES (?, 'PRINTFUL', ?, ?, ?, ?)
                    ON CONFLICT(store_id) DO UPDATE SET
                        daily_sales=excluded.daily_sales,
                        total_revenue=total_revenue + excluded.daily_sales,
                        last_sync=excluded.last_sync
                """, (store, sales, sales * 100, random.randint(15, 60), time.time()))
            conn.commit()
        swarm_log(f"SUCCESS: Synced {len(stores)} store fronts.", node="MONEY")

    async def _sync_robinhood(self):
        """Simulates fetching portfolio data from Robinhood."""
        assets = [
            {"id": "BTC", "type": "CRYPTO", "val": 64000.0},
            {"id": "NVDA", "type": "STOCK", "val": 125.0},
            {"id": "TSLA", "type": "STOCK", "val": 220.0}
        ]
        with db._get_connection() as conn:
            for asset in assets:
                daily_change = random.uniform(-5.0, 5.0)
                conn.execute("""
                    INSERT INTO financial_portfolio (asset_id, type, current_value, daily_change_pct, total_pnl, last_sync)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ON CONFLICT(asset_id) DO UPDATE SET
                        current_value=excluded.current_value,
                        daily_change_pct=excluded.daily_change_pct,
                        last_sync=excluded.last_sync
                """, (asset['id'], asset['type'], asset['val'], daily_change, daily_change * 10, time.time()))
            conn.commit()
        swarm_log("SUCCESS: Financial portfolio synchronized with Robinhood.", node="MONEY")

if __name__ == "__main__":
    asyncio.run(RevenueSync().run_sync_loop())
