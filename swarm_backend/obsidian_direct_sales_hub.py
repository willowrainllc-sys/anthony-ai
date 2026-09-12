# --- WILLOW RAIN COMPANY LLC: OBSIDIAN DIRECT-SALES HUB v1.0 ---
import os
import sys
import json
import uuid
import time
import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path

from swarm_logger import swarm_log
from swarm_persistence import db
from square_checkout_gateway import square_gateway
from obsidian_infrastructure_controller import infra_controller
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
SALES_VAULT = SECURE_DIR / "direct_sales_vault"
SALES_VAULT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. DIRECT SALES & CONTRACT SCHEMAS
# ============================================================

class ServiceContract(BaseModel):
    contract_id: str
    client_entity: str
    service_type: str          # "PRIVATE_PROXY_PORT", "CUSTOM_AI_DATASET", "COMPUTE_SLICE"
    monthly_fee_usd: float
    billing_status: str = "INVOICED"
    checkout_url: str
    timestamp: float = Field(default_factory=time.time)

class ObsidianDirectSalesHub:
    """
    OBSIDIAN DIRECT-SALES HUB v1.0:
    Bypasses the "Aggregator" middlemen (Geonode/Rayobyte) and allows companies
    to buy Willow Rain services DIRECTLY from you.
    1. SERVICE CATALOG: Lists your 16-port matrix and 10-node compute cluster as a product.
    2. INSTANT ONBOARDING: Generates a contract and a Square payment link in 1 click.
    3. REVENUE RETENTION: You keep 100% of the profit (No 30% aggregator fee).
    """
    async def create_direct_b2b_contract(self, company_name: str, service: str = "PRIVATE_PROXY_PORT") -> ServiceContract:
        swarm_log(f"DIRECT_SALES: Drafting direct contract for [{company_name}]...", node="SALES_HUB")

        # Premium Direct Pricing
        pricing = {
            "PRIVATE_PROXY_PORT": 250.00,
            "CUSTOM_AI_DATASET": 899.00,
            "COMPUTE_SLICE": 450.00
        }

        fee = pricing.get(service, 250.00)
        contract_id = f"WR-DIR-{uuid.uuid4().hex[:6].upper()}"

        # Generate Square Checkout for the Direct Sale
        sq_res = await square_gateway.create_digital_product_checkout(f"Willow Rain Direct Service: {service}", fee)

        contract = ServiceContract(
            contract_id=contract_id,
            client_entity=company_name,
            service_type=service,
            monthly_fee_usd=fee,
            checkout_url=sq_res.get("checkout_url")
        )

        db.log_event("SALES_HUB", "DIRECT_CONTRACT_CREATED", contract.model_dump())

        swarm_log(f" SALES_HUB SUCCESS: Direct contract [{contract_id}] live for [{company_name}]! Fee: ${fee:,.2f} USD.", node="SALES_HUB")
        return contract

    def generate_direct_sales_portal_metadata(self) -> dict:
        """Returns the data needed to build your professional landing page."""
        return {
            "business_name": "Willow Rain Company LLC",
            "available_ips": 10,
            "network_status": "OBSIDIAN_LOCKED_100",
            "uptime_verified": "99.99%",
            "direct_checkout_link": "https://square.link/u/8EXWFidA"
        }

direct_sales_hub = ObsidianDirectSalesHub()

if __name__ == "__main__":
    async def test_sales():
        contract = await direct_sales_hub.create_direct_b2b_contract("Data_Research_Group", "CUSTOM_AI_DATASET")
        print("\n=== [SUPREME] WILLOW RAIN DIRECT B2B CONTRACT ===")
        print("Contract ID:", contract.contract_id)
        print("Client:", contract.client_entity)
        print("Monthly Fee:", f"${contract.monthly_fee_usd:,.2f}")
        print("PAYMENT LINK:", contract.checkout_url)

    asyncio.run(test_sales())
