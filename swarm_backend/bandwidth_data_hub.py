# --- WILLOW RAIN ENTERPRISES: BANDWIDTH DATA HUB & SPACE MANAGER v1.0 ---
import os
import sys
import json
import uuid
import time
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from pathlib import Path

from swarm_logger import swarm_log
from swarm_persistence import db
from square_checkout_gateway import square_gateway
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SQUARE_LOC = os.getenv("SQUARE_LOCATION_ID", "LDCKH8QA4MVA4")
SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
HUB_VAULT = SECURE_DIR / "bandwidth_data_hubs"
HUB_VAULT.mkdir(parents=True, exist_ok=True)

# YOUR OWNED & REGISTERED BANDWIDTH SPACES
REGISTERED_BANDWIDTH_SPACES = [
    {"space_id": "HUB_SPACE_01", "name": "Willow Rain Midwest Space #1", "ip": "192.168.1.101", "port": 1080, "type": "SOCKS5_DATA_HUB", "status": "READY"},
    {"space_id": "HUB_SPACE_02", "name": "Willow Rain Midwest Space #2", "ip": "192.168.1.102", "port": 1081, "type": "HTTP_DATA_HUB", "status": "READY"},
    {"space_id": "HUB_SPACE_03", "name": "Willow Rain Midwest Space #3", "ip": "192.168.1.103", "port": 1082, "type": "SOCKS5_DATA_HUB", "status": "READY"},
    {"space_id": "HUB_SPACE_04", "name": "Willow Rain Midwest Space #4", "ip": "192.168.1.104", "port": 1083, "type": "HIGH_SPEED_PIPE", "status": "READY"}
]

class CompanySpaceAccess(BaseModel):
    access_id: str
    company_name: str
    assigned_space_id: str
    endpoint_credentials: str
    monthly_rate_usd: float
    checkout_url: str

class BandwidthDataHubManager:
    """
    BANDWIDTH DATA HUB MANAGER v1.0:
    Direct, simple management of your owned bandwidth spaces & server nodes.
    Issues company connection credentials and processes direct Square rent payments.
    """
    def __init__(self):
        self.spaces = REGISTERED_BANDWIDTH_SPACES

    def get_registered_spaces(self) -> list:
        return self.spaces

    async def rent_bandwidth_space_to_company(self, company_name: str, plan_type: str = "starter") -> CompanySpaceAccess:
        """Assigns an owned bandwidth space to a company and generates a direct 1-click Square payment link."""
        space = random.choice(self.spaces)
        access_id = f"access_{uuid.uuid4().hex[:6]}"
        price = 99.00 if plan_type.lower() == "enterprise" else 29.00
        plan_label = f"Willow Rain Bandwidth Space Rental ({space['name']})"

        swarm_log(f"BANDWIDTH_HUB: Renting [{space['name']}] to company [{company_name}] for ${price}/mo...", node="BW_HUB")

        sq_res = await square_gateway.create_digital_product_checkout(plan_label, price)

        creds = f"socks5://{company_name.lower().replace(' ', '')}:{uuid.uuid4().hex[:8]}@{space['ip']}:{space['port']}"

        access_obj = CompanySpaceAccess(
            access_id=access_id,
            company_name=company_name,
            assigned_space_id=space["space_id"],
            endpoint_credentials=creds,
            monthly_rate_usd=price,
            checkout_url=sq_res.get("checkout_url")
        )

        out_file = HUB_VAULT / f"{access_id}.json"
        with open(out_file, "w") as f:
            f.write(access_obj.model_dump_json(indent=4))

        db.log_event("BW_HUB", "BANDWIDTH_SPACE_RENTED", {
            "company_name": company_name,
            "space_id": space["space_id"],
            "monthly_price_usd": price,
            "vault_path": str(out_file)
        })

        swarm_log(f" BANDWIDTH_HUB SUCCESS: Space [{space['space_id']}] rented to {company_name} (${price}/mo)!", node="BW_HUB")
        return access_obj

import random
bandwidth_hub = BandwidthDataHubManager()

if __name__ == "__main__":
    async def test_hub():
        res = await bandwidth_hub.rent_bandwidth_space_to_company("Acme Data Corp", "starter")
        print("BANDWIDTH DATA HUB RENTAL:")
        print("Company:", res.company_name)
        print("Assigned Space:", res.assigned_space_id)
        print("Connection Credentials:", res.endpoint_credentials)
        print("Square Payment Link:", res.checkout_url)

    asyncio.run(test_hub())
