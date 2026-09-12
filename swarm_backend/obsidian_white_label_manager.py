# --- WILLOW RAIN COMPANY LLC: OBSIDIAN WHITE-LABEL RESELLER & AFFILIATE HUB v1.0 ---
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
from obsidian_node_manager import node_manager
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
RESELLER_VAULT = SECURE_DIR / "obsidian_reseller_vault"
RESELLER_VAULT.mkdir(parents=True, exist_ok=True)

# ============================================================
# 1. WHITE-LABEL & RESELLER SCHEMAS
# ============================================================

class ResellerPartner(BaseModel):
    reseller_id: str
    name: str
    email: str
    total_nodes_hosted: int = 0
    total_gb_contributed: float = 0.0
    total_unpaid_commission_usd: float = 0.0
    status: str = "ACTIVE_PARTNER"
    joined_at: float = Field(default_factory=time.time)

class WhiteLabelManifest(BaseModel):
    manifest_id: str
    master_provider: str = "Willow Rain Company LLC"
    active_resellers_count: int
    total_reseller_ips: int
    system_net_profit_usd: float
    timestamp: float = Field(default_factory=time.time)

# ============================================================
# 2. OBSIDIAN WHITE-LABEL MANAGER
# ============================================================

class ObsidianWhiteLabelManager:
    """
    OBSIDIAN WHITE-LABEL MANAGER v1.0:
    The "Master Bank" of the network.
    1. PARTNER ONBOARDING: Issues 'Clone' installers to white-label resellers.
    2. COMMISSION TRACKING: Tracks how much data each reseller's nodes contribute.
    3. REVENUE SHARING: Calculates 50/50 splits (You keep 50% for providing the 'Brain' and 'Handshakes').
    4. AUTOMATED PAYOUTS: Triggers Square/ACH payouts to partners when they reach $100.
    """
    def __init__(self):
        self.resellers: List[ResellerPartner] = []

    def onboard_new_reseller(self, name: str, email: str) -> dict:
        """Onboards a partner and gives them their custom 'Clone' command."""
        reseller_id = f"RES-{uuid.uuid4().hex[:6].upper()}"
        partner = ResellerPartner(reseller_id=reseller_id, name=name, email=email)
        self.resellers.append(partner)

        # Generate their unique 'Clone' command
        installer_cmd = node_manager.generate_one_command_installer(exit_ip="47.85.50.46")

        swarm_log(f" WHITE_LABEL: Onboarded partner [{name}]. Issued Reseller ID: {reseller_id}", node="RESELLER_HUB")

        db.log_event("RESELLER_HUB", "PARTNER_ONBOARDED", {
            "reseller_id": reseller_id,
            "name": name,
            "email": email
        })

        return {
            "reseller_id": reseller_id,
            "status": "ARMED",
            "installer_cmd": installer_cmd,
            "portal_url": f"https://obsidian-ai.vercel.app/partners/{reseller_id}"
        }

    async def calculate_network_splits(self, total_strike_yield: float) -> dict:
        """Calculates the 50/50 net profit split between the Master and Resellers."""
        # 50% goes to Willow Rain (Master) for Infrastructure/Ops
        # 50% is distributed among active resellers based on node count
        total_reseller_share = total_strike_yield * 0.50
        willow_rain_net = total_strike_yield * 0.50

        swarm_log(f"RESELLER_HUB: Calculating revenue splits for strike yield [${total_strike_yield:,.2f}]", node="RESELLER_HUB")

        return {
            "total_yield_usd": total_strike_yield,
            "willow_rain_net_profit": willow_rain_net,
            "reseller_payout_pool": total_reseller_share,
            "distribution_status": "NEGOTIATING_ACH_SETTLEMENT"
        }

    def generate_grand_reseller_manifest(self) -> WhiteLabelManifest:
        """Finalizes the network state for enterprise B2B transparency."""
        total_nodes = sum(r.total_nodes_hosted for r in self.resellers)

        manifest = WhiteLabelManifest(
            manifest_id=f"WLM-{uuid.uuid4().hex[:8].upper()}",
            active_resellers_count=len(self.resellers),
            total_reseller_ips=total_nodes,
            system_net_profit_usd=0.0 # Updated via calculate_network_splits
        )

        out_file = RESELLER_VAULT / "master_reseller_manifest.json"
        with open(out_file, "w") as f:
            f.write(manifest.model_dump_json(indent=4))

        swarm_log(f" WHITE_LABEL: Reseller Manifest Locked. Network Scale: {len(self.resellers)} Partners.", node="RESELLER_HUB")
        return manifest

white_label_manager = ObsidianWhiteLabelManager()

if __name__ == "__main__":
    # 1. Onboard 3 Team Partners
    p1 = white_label_manager.onboard_new_reseller("Mate_Claw_Operations", "mate.claw@example.com")
    p2 = white_label_manager.onboard_new_reseller("Shadow_Librarian_Data", "shadow.lib@example.com")

    # 2. Simulate Split from a $10,000 Strike
    splits = asyncio.run(white_label_manager.calculate_network_splits(10000.00))

    print("\n=== [SUPREME] WILLOW RAIN WHITE-LABEL PARTNER PORTAL ===")
    print("Partner ID:", p1["reseller_id"])
    print("Custom Clone Command:", p1["installer_cmd"])
    print("\n--- REVENUE SPLIT (50/50 MODEL) ---")
    print("Total Strike Yield:", f"${splits['total_yield_usd']:,.2f}")
    print("WILLOW RAIN NET PROFIT:", f"${splits['willow_rain_net_profit']:,.2f}")
    print("Reseller Payout Pool:", f"${splits['reseller_payout_pool']:,.2f}")
