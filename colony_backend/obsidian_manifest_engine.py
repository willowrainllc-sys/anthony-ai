# --- WILLOW RAIN ENTERPRISES: OBSIDIAN SYSTEM MANIFEST & MASTER KEY VAULT v1.1 ---
import os
import sys
import json
import uuid
import time
from pathlib import Path
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from colony_logger import colony_log
from colony_persistence import db
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Colony\Secure_Assets")
MANIFEST_VAULT = SECURE_DIR / "obsidian_manifest"
MANIFEST_VAULT.mkdir(parents=True, exist_ok=True)

class ObsidianKeys(BaseModel):
    alibaba_cloud: Dict[str, str] = Field(default_factory=dict)
    square_merchant: Dict[str, str] = Field(default_factory=dict)
    supabase_vault: Dict[str, str] = Field(default_factory=dict)
    youtube_broadcast: Dict[str, str] = Field(default_factory=dict)
    wallets: Dict[str, str] = Field(default_factory=dict)
    meta_social: Dict[str, str] = Field(default_factory=dict)

class ObsidianArchitecture(BaseModel):
    build_os: str = "v5.0 (build_brain_architecture.py)"
    central_brain: str = "v4.0 (colony_brain.py)"
    media_studio: str = "v16.0 (pipeline.py / story_director_v2.py)"
    network_engine: str = "v5.0 (opensource_traffic_stack.py / visual_director_v4.py)"
    settlement_hub: str = "v2.1 (direct_settlement_wallet_hub.py)"
    transparency_hub: str = "v1.0 (cl4r1t4s_transparency_engine.py)"
    automation_daemon: str = "v5.0 (daemon_worker.py)"

class ObsidianSystemManifest(BaseModel):
    manifest_id: str
    owner: str = "Obsidian AI / Willow Rain Company LLC"
    timestamp: float = Field(default_factory=time.time)
    keys: ObsidianKeys
    architecture: ObsidianArchitecture
    endpoints: Dict[str, str]
    status: str = "OBSIDIAN_SYSTEM_LOCKED_AND_ACTIVE"

class ObsidianManifestEngine:
    """
    OBSIDIAN MANIFEST ENGINE v1.1:
    Consolidates every key, endpoint, and architectural component into a single
    Master Knowledge Manifest for the Central Brain to reference and control.
    """
    def generate_master_manifest(self) -> ObsidianSystemManifest:
        colony_log("OBSIDIAN: Compiling Master System Manifest & Key Vault...", node="OBSIDIAN")

        keys = ObsidianKeys(
            alibaba_cloud={
                "access_key_id": os.getenv("ALIBABA_ACCESS_KEY_ID", ""),
                "public_eip": os.getenv("ALIBABA_EIP", "47.85.50.46")
            },
            square_merchant={
                "location_id": os.getenv("SQUARE_LOCATION_ID", "LDCKH8QA4MVA4"),
                "merchant_name": "Willow Rain Company LLC"
            },
            supabase_vault={
                "url": os.getenv("SUPABASE_URL", ""),
                "key": os.getenv("SUPABASE_KEY", "")[:10] + "..."
            },
            youtube_broadcast={
                "channel_id": os.getenv("YOUTUBE_CHANNEL_ID", "UCyIaZjMUZJHDqLtP1wh5Iuw")
            },
            wallets={
                "polygon_usdc": "0xWillowRainPolygonUSDCWallet2026",
                "solana_usdc": "WillowRainSolanaUSDCWallet2026",
                "multi_sig": "0xWillowRainMultiSigColdStorage2026"
            },
            meta_social={
                "facebook_page_id": os.getenv("FACEBOOK_PAGE_ID", ""),
                "instagram_id": os.getenv("INSTAGRAM_BUSINESS_ACCOUNT_ID", "")
            }
        )

        endpoints = {
            "web_portal": os.getenv("VERCEL_URL", "https://obsidian.city"),
            "fastmcp_gateway": "http://localhost:8000",
            "comfyui_render": os.getenv("COMFY_URL", "http://127.0.0.1:8188"),
            "ingress_gateway": f"socks5://{keys.alibaba_cloud['public_eip']}:1080"
        }

        manifest = ObsidianSystemManifest(
            manifest_id=f"manifest_{uuid.uuid4().hex[:8].upper()}",
            keys=keys,
            architecture=ObsidianArchitecture(),
            endpoints=endpoints
        )

        # Save Manifest to Secure Vault
        out_file = MANIFEST_VAULT / f"master_manifest.json"
        with open(out_file, "w") as f:
            f.write(manifest.model_dump_json(indent=4))

        # Log to Database
        db.log_event("OBSIDIAN", "SYSTEM_MANIFEST_COMPILED", {
            "manifest_id": manifest.manifest_id,
            "timestamp": manifest.timestamp,
            "vault_path": str(out_file)
        })

        colony_log(f" OBSIDIAN SUCCESS: Master Manifest [{manifest.manifest_id}] Locked & Loaded for Central Brain!", node="OBSIDIAN")
        return manifest

obsidian_engine = ObsidianManifestEngine()

if __name__ == "__main__":
    m = obsidian_engine.generate_master_manifest()
    print("OBSIDIAN MASTER MANIFEST:")
    print(json.dumps(json.loads(m.model_dump_json()), indent=2))
