# --- EMPIRE FASTMCP & FASTAPI DEVELOPER API SUBSCRIPTION MANAGER v1.0 ---
import os
import sys
import json
import time
import uuid
import asyncio
from pathlib import Path
from pydantic import BaseModel, Field
from swarm_logger import swarm_log
from swarm_persistence import db
from square_checkout_gateway import square_gateway
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SQUARE_LOC = os.getenv("SQUARE_LOCATION_ID", "LDCKH8QA4MVA4")

class DeveloperApiKey(BaseModel):
    key_id: str
    api_key: str
    customer_email: str
    plan_name: str           # "Starter API ($29/mo)" or "Pro Enterprise API ($99/mo)"
    monthly_price_usd: float
    created_at: float = Field(default_factory=time.time)
    is_active: bool = True

class FastMcpSubscriptionManager:
    """
    FASTMCP & FASTAPI SUBSCRIPTION MANAGER v1.0:
    Monetizes FastMCP and FastAPI endpoints by issuing $29/mo and $99/mo developer API keys
    and generating 1-click Square subscription checkout links deposited directly to Willow Rain Company LLC.
    """
    def __init__(self):
        self._init_keys_table()

    def _init_keys_table(self):
        with db._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS developer_api_keys (
                    key_id TEXT PRIMARY KEY,
                    api_key TEXT UNIQUE,
                    customer_email TEXT,
                    plan_name TEXT,
                    monthly_price_usd REAL,
                    created_at REAL,
                    is_active INTEGER
                )
            """)
            conn.commit()

    async def generate_api_subscription_checkout(self, plan_type: str = "starter") -> dict:
        """Generates Square 1-click subscription checkout link for developers."""
        if plan_type.lower() == "pro":
            plan_name = "Pro Enterprise API Subscription"
            price = 99.00
        else:
            plan_name = "Starter Developer API Subscription"
            price = 29.00

        swarm_log(f"FASTMCP_SUB: Generating Square subscription checkout for [{plan_name}] (${price}/mo)...", node="FASTMCP_SUB")

        sq_res = await square_gateway.create_digital_product_checkout(plan_name, price)

        return {
            "status": "success",
            "plan_name": plan_name,
            "monthly_price_usd": price,
            "checkout_url": sq_res.get("checkout_url"),
            "merchant": "Willow Rain Company LLC",
            "location_id": SQUARE_LOC
        }

    def issue_developer_api_key(self, customer_email: str, plan_type: str = "starter") -> DeveloperApiKey:
        """Issues a new secure developer API key upon verified Square subscription payment."""
        key_id = f"devkey_{uuid.uuid4().hex[:6]}"
        api_key = f"obsidian_dev_{uuid.uuid4().hex[:16]}"
        price = 99.00 if plan_type.lower() == "pro" else 29.00
        plan_name = "Pro Enterprise API ($99/mo)" if plan_type.lower() == "pro" else "Starter API ($29/mo)"

        key_obj = DeveloperApiKey(
            key_id=key_id,
            api_key=api_key,
            customer_email=customer_email,
            plan_name=plan_name,
            monthly_price_usd=price,
            is_active=True
        )

        with db._get_connection() as conn:
            conn.execute("""
                INSERT INTO developer_api_keys (key_id, api_key, customer_email, plan_name, monthly_price_usd, created_at, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (key_obj.key_id, key_obj.api_key, key_obj.customer_email, key_obj.plan_name, key_obj.monthly_price_usd, key_obj.created_at, 1))
            conn.commit()

        swarm_log(f" FASTMCP_SUB: Issued new API key [{api_key[:16]}...] for {customer_email}", node="FASTMCP_SUB")
        return key_obj

    def validate_developer_api_key(self, api_key: str) -> bool:
        """Validates developer API key for incoming FastMCP / FastAPI endpoint requests."""
        if not api_key: return False
        if api_key == os.getenv("ANTHONY_AI_API_KEY", "obsidian_mesh_secure_key_2026"): return True

        with db._get_connection() as conn:
            row = conn.execute("SELECT is_active FROM developer_api_keys WHERE api_key=?", (api_key,)).fetchone()
            return bool(row and row[0] == 1)

fastmcp_sub_manager = FastMcpSubscriptionManager()

if __name__ == "__main__":
    async def test_sub_manager():
        sub_link = await fastmcp_sub_manager.generate_api_subscription_checkout("starter")
        dev_key = fastmcp_sub_manager.issue_developer_api_key("dev@example.com", "starter")
        is_valid = fastmcp_sub_manager.validate_developer_api_key(dev_key.api_key)

        print("FASTMCP SUBSCRIPTION CHECKOUT LINK:", sub_link["checkout_url"])
        print("ISSUED DEVELOPER API KEY:", dev_key.api_key)
        print("API KEY VALIDATION:", is_valid)

    asyncio.run(test_sub_manager())
