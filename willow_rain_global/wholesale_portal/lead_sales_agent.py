# --- OBSIDIAN GLOBAL: LEAD SALES AGENT v2.1 (FIXED IMPORTS) ---
import asyncio
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Absolute Path Correction
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
load_dotenv(ROOT / ".env")
sys.path.append(str(ROOT / "swarm_backend"))
sys.path.append(str(ROOT / "willow_rain_global" / "cellular_stack"))

from swarm_logger import swarm_log
from swarm_persistence import db

class LeadSalesAgent:
    """
    LEAD SALES AGENT v2.1:
    The "Boss Mode" liquidation engine.
    """
    async def execute_sales_strike(self, niche="Missouri"):
        swarm_log(f"SALES: Initiating REAL-WORLD liquidation strike for [{niche}] leads...", node="SUPREME")

        # 1. Target Buyer
        client_name = "St. Louis Direct Marketing"
        email = "procurement@stldm.com"

        # 2. Calculate Payout (50 leads @ $1.25)
        amount = 62.50

        # 3. Physically PUBLISH Invoice to Square
        from square_checkout_gateway import square_gateway
        res = await square_gateway.create_and_publish_invoice(
            client_name=client_name,
            email=email,
            amount_usd=amount,
            description=f"Imperium Elite Identity Batch: {niche} (50 IDs)"
        )

        if res.get("status") == "success":
            swarm_log(f"✓ SALES SUCCESS: Invoice for ${amount} published at 'willow rain Co'.", node="SUPREME")
            db.log_event("SALES", "INVOICE_PUBLISHED", {"client": client_name, "amount": amount, "invoice_id": res['invoice_id']})
        else:
            swarm_log(f"[-] SALES ERROR: {res.get('message')}", node="SUPREME")

sales_agent = LeadSalesAgent()

if __name__ == "__main__":
    asyncio.run(sales_agent.execute_sales_strike())
