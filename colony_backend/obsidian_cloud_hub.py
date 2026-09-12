# --- WILLOW RAIN COMPANY LLC: OBSIDIAN CLOUD HUB & DATA WAREHOUSE MASTER v1.0 ---
import os
import sys
import json
import uuid
import time
import random
import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path

from colony_logger import colony_log
from colony_persistence import db
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Colony\Secure_Assets")
HUB_VAULT = SECURE_DIR / "obsidian_cloud_vault"
HUB_VAULT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. OBSIDIAN RESOURCE & DATA SPACE SCHEMAS
# ============================================================

class DataSpace(BaseModel):
    space_id: str
    category: str              # "AI_INFERENCE", "MARKET_PULSE", "PROXY_EXIT", "WAREHOUSE_STORAGE"
    allocated_capacity: str    # e.g. "100GB", "24-Core GPU", "10Gbps Uplink"
    assigned_company: str = "AVAILABLE"
    monthly_yield_usd: float
    status: str = "PROVISIONED"

class ObsidianCloudManifest(BaseModel):
    manifest_id: str
    provider: str = "Willow Rain Company LLC"
    active_spaces: List[DataSpace]
    total_monthly_gross_usd: float
    timestamp: float = Field(default_factory=time.time)

# ============================================================
# 2. OBSIDIAN CLOUD HUB MASTER
# ============================================================

class ObsidianCloudHubMaster:
    """
    OBSIDIAN CLOUD HUB MASTER v1.0:
    The direct B2B IaaS (Infrastructure as a Service) layer for Willow Rain Company LLC.
    Companies buy access to specialized "Data Spaces" rather than just raw bandwidth.

    HIGH-AURA REVENUE CHANNELS:
    1. AI INFERENCE SPACE: Renting GPU/NPU compute for LLM/ComfyUI workloads.
    2. MARKET PULSE SPACE: Real-time financial/OSINT data pipelines.
    3. PROXY EXIT SPACE: High-density, unflagged residential routing.
    4. WAREHOUSE STORAGE: Encrypted, decentralized data archiving.
    """
    def __init__(self):
        self.manifest_id = f"HUB-{uuid.uuid4().hex[:8].upper()}"
        self.spaces = [
            # 1. AI Inference Cluster
            DataSpace(space_id="AI-01", category="AI_INFERENCE", allocated_capacity="NVIDIA H100 Instance (Virtual)", monthly_yield_usd=1200.00),
            DataSpace(space_id="AI-02", category="AI_INFERENCE", allocated_capacity="LLM-8B Dedicated Buffer", monthly_yield_usd=450.00),

            # 2. Market Pulse Pipelines
            DataSpace(space_id="MP-01", category="MARKET_PULSE", allocated_capacity="1M Records / Day OSINT Feed", monthly_yield_usd=899.00),
            DataSpace(space_id="MP-02", category="MARKET_PULSE", allocated_capacity="High-Freq Ticker Relay", monthly_yield_usd=1500.00),

            # 3. Premium Proxy Exit nodes
            DataSpace(space_id="PX-01", category="PROXY_EXIT", allocated_capacity="10Gbps Multi-IP Port Matrix", monthly_yield_usd=2500.00),

            # 4. Data Warehouse Storage
            DataSpace(space_id="DW-01", category="WAREHOUSE_STORAGE", allocated_capacity="100TB Cold Vault", monthly_yield_usd=950.00)
        ]

    async def execute_provisioning_pulse(self):
        """Simulates the check of all provisioned spaces and their yield generation."""
        colony_log("HUB_MASTER: Auditing Obsidian Cloud Data Spaces...", node="HUB_MASTER")

        occupied_spaces = [s for s in self.spaces if s.assigned_company != "AVAILABLE"]
        total_yield = sum(s.monthly_yield_usd for s in occupied_spaces)

        db.log_event("HUB_MASTER", "CLOUD_YIELD_AUDIT_COMPLETE", {
            "occupied_count": len(occupied_spaces),
            "total_monthly_yield": total_yield,
            "manifest_id": self.manifest_id
        })

        colony_log(f" HUB_MASTER SUCCESS: Obsidian Cloud Hub Active. Current Monthly Yield: ${total_yield:,.2f}", node="HUB_MASTER")
        return total_yield

    def lease_space_to_entity(self, space_id: str, company_name: str) -> Optional[DataSpace]:
        """Locks a specific data space to a corporate entity."""
        space = next((s for s in self.spaces if s.space_id == space_id), None)
        if space:
            space.assigned_company = company_name
            colony_log(f" HUB_MASTER: Space [{space_id}] leased to [{company_name}] for ${space.monthly_yield_usd}/mo.", node="HUB_MASTER")
            return space
        return None

    def generate_grand_manifest(self) -> ObsidianCloudManifest:
        """Finalizes the master manifest for B2B accounting."""
        occupied_sum = sum(s.monthly_yield_usd for s in self.spaces if s.assigned_company != "AVAILABLE")

        manifest = ObsidianCloudManifest(
            manifest_id=self.manifest_id,
            active_spaces=self.spaces,
            total_monthly_gross_usd=occupied_sum
        )

        out_file = HUB_VAULT / f"{self.manifest_id}_grand_manifest.json"
        with open(out_file, "w") as f:
            f.write(manifest.model_dump_json(indent=4))

        colony_log(f" HUB_MASTER: Grand Manifest [{self.manifest_id}] Locked & Vaulted.", node="HUB_MASTER")
        return manifest

hub_master = ObsidianCloudHubMaster()

if __name__ == "__main__":
    # 1. Lease spaces to high-value partners
    hub_master.lease_space_to_entity("AI-01", "OpenAI_Data_Lab")
    hub_master.lease_space_to_entity("MP-02", "Refinitiv_Finance")
    hub_master.lease_space_to_entity("PX-01", "Titan_Network_Wholesale")

    # 2. Run Audit Pulse
    asyncio.run(hub_master.execute_provisioning_pulse())

    # 3. Finalize Manifest
    m = hub_master.generate_grand_manifest()

    print("\n=== [SUPREME] WILLOW RAIN OBSIDIAN CLOUD HUB ===")
    print("Manifest ID:", m.manifest_id)
    print("Active Leases:", sum(1 for s in m.active_spaces if s.assigned_company != "AVAILABLE"))
    print("PROJECTED MONTHLY GROSS:", f"${m.total_monthly_gross_usd:,.2f}")
    print("Vault Path:", HUB_VAULT)
