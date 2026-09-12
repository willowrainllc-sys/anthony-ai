# --- WILLOW RAIN COMPANY LLC: OBSIDIAN SUBSCRIPTION VAULT (The Queen Bee's Layer) v1.0 ---
import os
import sys
import json
import uuid
import time
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from pathlib import Path

from swarm_logger import swarm_log
from swarm_persistence import db
from square_checkout_gateway import square_gateway

class SubscriptionTier(BaseModel):
    tier_id: str
    name: str
    price_usd: float
    features: List[str]
    status: str = "ACTIVE"

class ObsidianSubscriptionVault:
    """
    THE QUEEN BEE'S VAULT v1.0:
    The highest-margin recurring revenue stream.
    1. EXCLUSIVE ACCESS: A members-only area for 'Deep Lore' and 'Grid Intelligence'.
    2. RECURRING YIELD: Monthly $99 - $499 subscriptions for high-ticket data.
    3. AUTOMATED ONBOARDING: Pushes new members directly into the B2B portal.
    """
    def __init__(self):
        self.tiers = [
            SubscriptionTier(
                tier_id="T1-LORE",
                name="Obsidian Insider (Deep Lore)",
                price_usd=99.00,
                features=["Weekly Unclassified Dossiers", "4K Documentary Archives", "Exclusive Discord Access"]
            ),
            SubscriptionTier(
                tier_id="T2-GRID",
                name="Grid Commander (B2B Intel)",
                price_usd=499.00,
                features=["Real-time Threat Intel Feed", "Custom Data Scrapers", "Direct Proxy Hub Access"]
            )
        ]

    async def issue_membership_payout_link(self, tier_id: str) -> dict:
        tier = next((t for t in self.tiers if t.tier_id == tier_id), self.tiers[0])
        swarm_log(f"SUBSCRIPTION: Generating checkout for [{tier.name}]...", node="VAULT")

        sq_res = await square_gateway.create_digital_product_checkout(f"Willow Rain Subscription: {tier.name}", tier.price_usd)

        return {
            "name": tier.name,
            "monthly_fee": tier.price_usd,
            "checkout_url": sq_res.get("checkout_url")
        }

sub_vault = ObsidianSubscriptionVault()

if __name__ == "__main__":
    import asyncio
    async def test_sub():
        res = await sub_vault.issue_membership_payout_link("T2-GRID")
        print("\n=== [SUPREME] THE QUEEN BEE'S VAULT ===")
        print("Tier:", res["name"])
        print("Monthly Yield:", f"${res['monthly_fee']:.2f}")
        print("PAYMENT LINK:", res["checkout_url"])

    asyncio.run(test_sub())
