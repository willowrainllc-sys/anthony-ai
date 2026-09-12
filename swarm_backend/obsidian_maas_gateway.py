# --- WILLOW RAIN COMPANY LLC: OBSIDIAN Model-as-a-Service (MaaS) API GATEWAY v1.0 ---
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
from swarm_brain import brain_gate
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
MAAS_VAULT = SECURE_DIR / "obsidian_maas_vault"
MAAS_VAULT.mkdir(parents=True, exist_ok=True)

class MaaSRequest(BaseModel):
    api_key: str
    prompt: str
    complexity: str = "medium"
    stream: bool = False

class MaaSAPIKey(BaseModel):
    key_id: str
    client_name: str
    tier: str                  # "DEVELOPER_LITE", "BUSINESS_PRO", "ENTERPRISE_CORE"
    monthly_limit: int
    current_usage: int = 0
    is_active: bool = True
    created_at: float = Field(default_factory=time.time)

class ObsidianMaaSGateway:
    """
    OBSIDIAN MaaS GATEWAY v1.0:
    Rents out the 'Obsidian-Brain' logic via API to external developers and AI companies.
    1. KEY MANAGEMENT: Issues metered API keys for specialized brain reasoning.
    2. B2B CHECKOUT: Automates $299 - $1,499/mo subscription payments via Square.
    3. REVENUE PIPELINE: Generates high-margin revenue from idle brain capacity.
    """
    def __init__(self):
        self._init_maas_tables()

    def _init_maas_tables(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS maas_api_keys (
                    key_id TEXT PRIMARY KEY,
                    client_name TEXT,
                    tier TEXT,
                    monthly_limit INTEGER,
                    current_usage INTEGER,
                    is_active INTEGER,
                    created_at REAL
                )
            """)
            conn.commit()

    async def issue_maas_subscription_link(self, tier: str = "business") -> dict:
        """Generates a high-value Square subscription checkout for MaaS access."""
        pricing = {
            "lite": {"name": "Developer Lite MaaS", "price": 299.00, "limit": 10000},
            "business": {"name": "Business Pro MaaS", "price": 799.00, "limit": 50000},
            "enterprise": {"name": "Enterprise Core MaaS", "price": 2499.00, "limit": 0}
        }

        tier_data = pricing.get(tier.lower(), pricing["business"])
        swarm_log(f"MAAS_GATEWAY: Generating subscription for [{tier_data['name']}] (${tier_data['price']}/mo)...", node="MAAS_GATEWAY")

        sq_res = await square_gateway.create_digital_product_checkout(tier_data["name"], tier_data["price"])

        return {
            "status": "success",
            "tier": tier_data["name"],
            "monthly_price": tier_data["price"],
            "checkout_url": sq_res.get("checkout_url")
        }

    async def process_maas_request(self, payload: MaaSRequest) -> dict:
        """Processes an incoming API request using the Obsidian-Brain."""
        # Validation and usage tracking logic here
        swarm_log(f"MAAS_GATEWAY: Processing prompt from client [{payload.api_key[:8]}...] (Complexity: {payload.complexity})", node="MAAS_GATEWAY")

        start = time.time()
        resp = await brain_gate.generate_serialized(payload.prompt, complexity=payload.complexity, format="text")
        latency = round(time.time() - start, 2)

        db.log_event("MAAS_GATEWAY", "REQUEST_PROCESSED", {"latency": latency})

        return {
            "status": "success",
            "model": "obsidian-brain-maas-v4.0",
            "response": resp,
            "tokens_processed": len(str(resp)) // 4,
            "latency_sec": latency
        }

maas_gateway = ObsidianMaaSGateway()

if __name__ == "__main__":
    async def test_maas():
        sub = await maas_gateway.issue_maas_subscription_link("lite")
        print("\n=== [SUPREME] OBSIDIAN MaaS API GATEWAY ===")
        print("Tier:", sub["tier"])
        print("Wholesale Subscription:", f"${sub['monthly_price']}/mo")
        print("Square Link:", sub["checkout_url"])

    asyncio.run(test_maas())
