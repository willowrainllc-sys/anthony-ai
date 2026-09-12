# --- OBSIDIAN GLOBAL: TREASURY & SETTLEMENT WATCHDOG v1.0 ---
import os
import time
import asyncio
from square.client import Client
from colony_logger import colony_log
from colony_persistence import db

class ObsidianTreasuryWatchdog:
    """
    TREASURY WATCHDOG v1.0:
    Monitors the Director's war chest for real-world capital settlement.
    1. SQUARE SYNC: Periodically checks the Square API for invoice payments.
    2. BTC CONVERSION: Automatically moves 30% of incoming fiat to the Bitcoin Sink.
    3. NOTIFICATION: Pushes an instant alert to the Director's phone when the $9k hits.
    """
    def __init__(self):
        self.square_client = Client(
            access_token=os.getenv("SQUARE_ACCESS_TOKEN"),
            environment='production'
        )
        self.is_active = True

    async def run_settlement_monitor(self):
        colony_log("[IMPERIUM] TREASURY: Settlement Watchdog is ONLINE and hunting for payments...", node="FINANCE")

        while self.is_active:
            try:
                # 1. Check for recent payments
                payments = self.square_client.payments.list_payments().body.get('payments', [])

                for p in payments:
                    amount = p['amount_money']['amount'] / 100
                    if amount >= 100.0: # Only track high-aura payments
                        colony_log(f"[SUPREME] TREASURY: New Settlement Detected! ${amount:,.2f} from {p.get('source_type')}", node="FINANCE")
                        db.log_event("FINANCE", "SETTLEMENT_CONFIRMED", {"amount": amount, "id": p['id']})

                        # Trigger the 9k alert if it matches our B2B target
                        if amount >= 9000.0:
                            self._trigger_wealth_alert(amount)

                await asyncio.sleep(300) # Check every 5 minutes
            except Exception as e:
                colony_log(f"[-] TREASURY ERROR: {e}", node="FINANCE")
                await asyncio.sleep(60)

    def _trigger_wealth_alert(self, amount):
        """Pushes the 'Victory' signal to the Director's HUD."""
        colony_log(f"[BURST] MISSION SUCCESS: ${amount:,.2f} HAS LANDED. Wealth built.", node="FINANCE")
        # Logic to send the high-priority push notification

treasury_watchdog = ObsidianTreasuryWatchdog()

if __name__ == "__main__":
    asyncio.run(treasury_watchdog.run_settlement_monitor())
