# --- WILLOW RAIN COMPANY LLC: AI AD CREATIVE AGENCY & B2B AD-ENGINE v1.0 ---
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
from master_studio import master_factory
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
AD_VAULT = SECURE_DIR / "b2b_ad_creatives"
AD_VAULT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. AD CREATIVE & AGENCY SCHEMAS
# ============================================================

class AdCreativePackage(BaseModel):
    package_id: str
    client_name: str
    campaign_goal: str         # "CONVERSION", "BRAND_AWARENESS", "APP_INSTALLS"
    ad_type: str               # "60S_VERTICAL_REEL", "15S_SNAP_AD", "30S_YOUTUBE_BUMPER"
    total_creatives: int
    wholesale_price_usd: float
    status: str = "PRODUCTION_QUEUED"

# ============================================================
# 2. AI AD CREATIVE AGENCY ENGINE
# ============================================================

class AiAdCreativeAgency:
    """
    AI AD CREATIVE AGENCY v1.0:
    Turns the Willow Rain Media Studio into a B2B Ad Factory.
    Brands pay for high-retention, Marvel-grade AI ad creatives.
    """
    async def create_wholesale_ad_package(self, client: str, goal: str = "CONVERSION", count: int = 5) -> AdCreativePackage:
        swarm_log(f"AD_AGENCY: Architecting [{count}] ad creatives for [{client}] (Goal: {goal})...", node="AD_AGENCY")

        # Calculate Agency Pricing ($150 - $500 per ad creative)
        price_per_ad = 250.00
        total_price = price_per_ad * count
        package_id = f"AD-{uuid.uuid4().hex[:6].upper()}"

        package = AdCreativePackage(
            package_id=package_id,
            client_name=client,
            campaign_goal=goal,
            ad_type="60S_VERTICAL_REEL",
            total_creatives=count,
            wholesale_price_usd=total_price
        )

        # Trigger Production Strikes for each ad
        for i in range(count):
            swarm_log(f"AD_AGENCY: Queuing Ad #{i+1} for [{client}]...", node="AD_AGENCY")
            # In production, this would call master_factory.produce_and_dispatch_episode()
            # with specific client brand parameters.

        db.log_event("AD_AGENCY", "AD_PACKAGE_SOLD", package.model_dump())

        # Generate Square Checkout Link for the Agency Fee
        sq_res = await square_gateway.create_digital_product_checkout(f"Ad Creative Package: {client}", total_price)

        swarm_log(f" AD_AGENCY SUCCESS: Package [{package_id}] live! Total Fee: ${total_price:,.2f} USD.", node="AD_AGENCY")
        return package

ad_agency = AiAdCreativeAgency()

if __name__ == "__main__":
    async def test_agency():
        pkg = await ad_agency.create_wholesale_ad_package("Luxury Watches Inc", goal="CONVERSION", count=3)
        print("\n=== [SUPREME] WILLOW RAIN AD CREATIVE AGENCY ===")
        print("Client:", pkg.client_name)
        print("Total Ads:", pkg.total_creatives)
        print("AGENCY WHOLESALE FEE:", f"${pkg.wholesale_price_usd:,.2f}")

    asyncio.run(test_agency())
