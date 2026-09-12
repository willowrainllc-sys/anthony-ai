# --- WILLOW RAIN COMPANY LLC: OBSIDIAN B2B OUTREACH DISPATCHER v1.0 ---
import os
import sys
import json
import uuid
import time
import asyncio
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db
from obsidian_lead_generator import lead_gen
from obsidian_direct_sales_hub import direct_sales_hub

class ObsidianOutreachDispatcher:
    """
    OBSIDIAN OUTREACH DISPATCHER v1.0:
    The "Sales Closer" for Willow Rain.
    1. LEAD PULL: Fetches high-intent leads from the lead generator.
    2. CONTRACT DRAFT: Automatically generates direct B2B contracts via the Sales Hub.
    3. EMAIL DISPATCH: Simulates sending the proposal and payment link to the client.
    """
    async def execute_automatic_outreach_strike(self, lead_category: str = "Real Estate"):
        swarm_log(f"OUTREACH: Initiating automatic sales strike for [{lead_category}]...", node="OUTREACH")

        # 1. Harvest & Pull Leads
        pkg = await lead_gen.harvest_high_intent_leads(lead_category)

        # Simulating processing 3 top leads from the package
        dispatch_count = 0
        for i in range(3):
            company = f"Lead_Entity_{uuid.uuid4().hex[:4].upper()}"

            # 2. Generate Direct Contract & Square Link
            contract = await direct_sales_hub.create_direct_b2b_contract(company, "PRIVATE_PROXY_PORT")

            # 3. Log Dispatch
            db.log_event("OUTREACH", "CONTRACT_DISPATCHED", {
                "client": company,
                "contract_id": contract.contract_id,
                "payment_url": contract.checkout_url
            })

            swarm_log(f" OUTREACH SUCCESS: Dispatched contract to [{company}]. Value: ${contract.monthly_fee_usd:,.2f}", node="OUTREACH")
            dispatch_count += 1

        return dispatch_count

outreach_dispatcher = ObsidianOutreachDispatcher()

if __name__ == "__main__":
    asyncio.run(outreach_dispatcher.execute_automatic_outreach_strike())
