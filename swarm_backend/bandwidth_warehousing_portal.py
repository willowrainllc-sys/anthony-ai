# --- WILLOW RAIN ENTERPRISES: BANDWIDTH WAREHOUSING & CLOUD PIPELINE PORTAL v1.0 ---
import os
import sys
import json
import uuid
import time
import random
import asyncio
from typing import List, Optional
from pydantic import BaseModel, Field
from pathlib import Path

from swarm_logger import swarm_log
from swarm_persistence import db
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
WAREHOUSE_VAULT = SECURE_DIR / "bandwidth_warehouses"
WAREHOUSE_VAULT.mkdir(parents=True, exist_ok=True)

# BANDWIDTH WAREHOUSE & SECURE PIPELINE REGISTRY
BANDWIDTH_WAREHOUSES = [
    {
        "warehouse_id": "WAREHOUSE_PIPE_01",
        "name": "Willow Rain Midwest 10Gbps Bandwidth Pipeline",
        "cloud_location": "US-Midwest Cloud Data Center",
        "capacity_tb": 100,
        "protocol": "SOCKS5_ENCRYPTED_GPRC",
        "endpoint": "47.85.50.46:8000",
        "status": "ONLINE_WAREHOUSE"
    },
    {
        "warehouse_id": "WAREHOUSE_PIPE_02",
        "name": "Willow Rain East Coast Secure Traffic Corridor",
        "cloud_location": "US-East Cloud Data Center",
        "capacity_tb": 250,
        "protocol": "HTTP2_SECURE_TUNNEL",
        "endpoint": "47.85.50.46:8001",
        "status": "ONLINE_WAREHOUSE"
    },
    {
        "warehouse_id": "WAREHOUSE_PIPE_03",
        "name": "Willow Rain EU High-Density Data Pipeline",
        "cloud_location": "EU-Central High-Speed Node",
        "capacity_tb": 500,
        "protocol": "DVPN_POLYGON_PIPE",
        "endpoint": "47.85.50.46:8002",
        "status": "ONLINE_WAREHOUSE"
    }
]

class WarehousePipelineAccess(BaseModel):
    access_token: str
    warehouse_name: str
    cloud_location: str
    allocated_bandwidth_tb: int
    secure_connection_endpoint: str
    status: str = "PIPELINE_ACTIVE"

class BandwidthWarehousingPortal:
    """
    BANDWIDTH WAREHOUSING & CLOUD PIPELINE PORTAL v1.0:
    Manages owned high-density cloud bandwidth warehouses and secure traffic corridors.
    Issues secure connection tokens for corporate buyers to run high-volume traffic through your cloud space.
    """
    def __init__(self):
        self.warehouses = BANDWIDTH_WAREHOUSES

    def get_warehouse_inventory(self) -> list:
        return self.warehouses

    def allocate_secure_pipeline_access(self, buyer_entity: str, capacity_tb: int = 10) -> WarehousePipelineAccess:
        warehouse = random.choice(self.warehouses)
        token = f"pipe_token_{uuid.uuid4().hex[:12]}"
        endpoint = f"socks5://dealer_{buyer_entity.lower().replace(' ', '')}:{token}@{warehouse['endpoint']}"

        swarm_log(f"WAREHOUSE: Allocating {capacity_tb} TB secure pipeline from [{warehouse['name']}] for [{buyer_entity}]...", node="WAREHOUSE")

        access_obj = WarehousePipelineAccess(
            access_token=token,
            warehouse_name=warehouse["name"],
            cloud_location=warehouse["cloud_location"],
            allocated_bandwidth_tb=capacity_tb,
            secure_connection_endpoint=endpoint,
            status="PIPELINE_ACTIVE"
        )

        out_file = WAREHOUSE_VAULT / f"{token}.json"
        with open(out_file, "w") as f:
            f.write(access_obj.model_dump_json(indent=4))

        db.log_event("WAREHOUSE", "PIPELINE_ACCESS_ALLOCATED", {
            "buyer": buyer_entity,
            "warehouse_id": warehouse["warehouse_id"],
            "capacity_tb": capacity_tb,
            "vault_path": str(out_file)
        })

        swarm_log(f" WAREHOUSE SUCCESS: Allocated {capacity_tb} TB pipeline token for {buyer_entity}!", node="WAREHOUSE")
        return access_obj

warehouse_portal = BandwidthWarehousingPortal()

if __name__ == "__main__":
    access = warehouse_portal.allocate_secure_pipeline_access("Global Enterprise Data Corp", capacity_tb=25)
    print("WILLOW RAIN BANDWIDTH WAREHOUSE PIPELINE ACCESS:")
    print("Warehouse Name:", access.warehouse_name)
    print("Cloud Location:", access.cloud_location)
    print("Allocated Bandwidth:", access.allocated_bandwidth_tb, "TB")
    print("Secure Connection Endpoint:", access.secure_connection_endpoint)
