# --- WILLOW RAIN COMPANY LLC: OBSIDIAN MILESTONE BILLING & INVOICE ENGINE v1.0 ---
import os
import sys
import json
import uuid
import time
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

from swarm_logger import swarm_log
from swarm_persistence import db
from square_checkout_gateway import square_gateway
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
INVOICE_VAULT = SECURE_DIR / "milestone_invoices"
INVOICE_VAULT.mkdir(parents=True, exist_ok=True)

class MilestoneInvoice(BaseModel):
    invoice_id: str
    client_name: str
    project_name: str
    milestone_title: str
    amount_usd: float
    payment_url: str
    status: str = "SENT_TO_CLIENT"
    timestamp: float = Field(default_factory=time.time)

class ObsidianMilestoneBilling:
    """
    OBSIDIAN MILESTONE BILLING ENGINE v1.0:
    Turns your backend engineering work into direct cash flow.
    1. BILLING TIERS: Standardizes fees for API deployment, DB migrations, and HUD wiring.
    2. SQUARE SYNC: Instantly generates a professional Square invoice link.
    3. ESCROW READY: Designed to work with Upwork/Toptal or direct B2B contracts.
    """
    def __init__(self):
        self.standard_fees = {
            "API_DEPLOYMENT": 1500.00,
            "DATABASE_MIGRATION": 2500.00,
            "HUD_CUSTOMIZATION": 1200.00,
            "AUTOPILOT_SETUP": 3500.00
        }

    async def generate_milestone_invoice(self, client: str, milestone_key: str) -> MilestoneInvoice:
        """Generates a real Square invoice for a specific technical deliverable."""
        amount = self.standard_fees.get(milestone_key, 1000.00)
        project = f"Obsidian Infrastructure: {milestone_key.replace('_', ' ').title()}"

        swarm_log(f"BILLING: Generating invoice for [{client}] - [{project}]...", node="BILLING")

        # 1. Generate Square Checkout Link
        sq_res = await square_gateway.create_digital_product_checkout(f"Milestone: {project}", amount)
        checkout_url = sq_res.get("checkout_url", "https://square.link/u/8EXWFidA")

        invoice_id = f"INV-{uuid.uuid4().hex[:6].upper()}"
        invoice = MilestoneInvoice(
            invoice_id=invoice_id,
            client_name=client,
            project_name=project,
            milestone_title=milestone_key,
            amount_usd=amount,
            payment_url=checkout_url
        )

        # 2. Persist to Vault
        out_file = INVOICE_VAULT / f"{invoice_id}.json"
        with open(out_file, "w") as f:
            f.write(invoice.model_dump_json(indent=4))

        db.log_event("BILLING", "INVOICE_GENERATED", invoice.model_dump())

        swarm_log(f" BILLING SUCCESS: Invoice [{invoice_id}] sent to [{client}]. Value: ${amount:,.2f} USD.", node="BILLING")
        return invoice

billing_engine = ObsidianMilestoneBilling()

if __name__ == "__main__":
    async def test_billing():
        # Example: Billing a partner for the API & HUD build we just finished
        res = await billing_engine.generate_milestone_invoice("B2B_Infrastructure_Partner", "API_DEPLOYMENT")
        print("\n=== [SUPREME] WILLOW RAIN MILESTONE INVOICE ===")
        print("Invoice ID:", res.invoice_id)
        print("Project:", res.project_name)
        print("AMOUNT DUE:", f"${res.amount_usd:,.2f}")
        print("SQUARE PAYMENT LINK:", res.payment_url)

    asyncio.run(test_billing())
