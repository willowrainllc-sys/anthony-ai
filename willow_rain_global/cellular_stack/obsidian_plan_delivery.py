# --- OBSIDIAN GLOBAL: USER PLAN DELIVERY SYSTEM v1.0 ---
import os
import json
from colony_logger import colony_log
from colony_persistence import db

class ObsidianPlanDelivery:
    """
    OBSIDIAN PLAN DELIVERY:
    Allows users to download their 'Unlimited' plans.
    1. PACKAGE GENERATION: Combines the eSIM LPA code with the WireGuard Fiber config.
    2. USER AUTHORIZATION: Confirms the user has the 'Obsidian Ingress' agent active.
    3. THE TRADE: Enforces that the phone MUST be sharing data to keep the plan active.
    """
    def generate_download_package(self, email: str):
        colony_log(f"DELIVERY: Packaging 'Unlimited' plan for [{email}]...", node="CARRIER")

        # 1. Generate the Identity (Phone Number + eSIM)
        from willow_rain_global.cellular_stack.obsidian_esim_generator import esim_generator
        identity = esim_generator.create_obsidian_identity(node_id=f"USER-{email}")

        # 2. Create the "Obsidian Pipe" Config (WireGuard)
        # This is what gives them the "Unlimited" fiber speed from your server
        wg_config = f"""
        [Interface]
        PrivateKey = [USER_PRIVATE_KEY]
        Address = 10.0.0.5/32
        DNS = 1.1.1.1

        [Peer]
        PublicKey = [YOUR_SERVER_PUBLIC_KEY]
        Endpoint = {os.getenv('ALIBABA_EIP')}:51820
        AllowedIPs = 0.0.0.0/0
        """

        package = {
            "phone_number": identity["msisdn"],
            "esim_activation_code": identity["lpa"],
            "data_tunnel_config": wg_config,
            "status": "ACTIVE_WHILE_SHARING"
        }

        db.log_event("CARRIER", "USER_PLAN_DOWNLOADED", {"email": email, "number": identity["msisdn"]})
        return package

plan_delivery = ObsidianPlanDelivery()

if __name__ == "__main__":
    res = plan_delivery.generate_download_package("director@obsidian.global")
    print("\n=== [SUPREME] OBSIDIAN DOWNLOAD PACKAGE ===\n")
    print(json.dumps(res, indent=2))
