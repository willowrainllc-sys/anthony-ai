# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v5.0 (LEGITIMACY ORCHESTRATOR) ---
import asyncio
import os
import sys
from pathlib import Path

# Fix paths for imports
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
sys.path.append(str(ROOT / "swarm_backend"))

from swarm_logger import swarm_log
from node_merchant_architect import MerchantArchitectNode
from node_seo_specialist import SEOSpecialistNode
from playwright_industrial_strikes import strike_engine

async def run_full_legitimacy_strike():
    swarm_log("🔱 LEGITIMACY: Initiating Global Professionalism Strike...", node="SUPREME")

    # 1. MERCHANT ARCHITECT: Ensure all 8 storefronts are published & mapped
    architect = MerchantArchitectNode()
    await architect.execute_merchant_strike(register=False) # Skip reg until keys provided

    # 2. SEO SPECIALIST: Ping global indexers for the current public bridge link
    bridge_url = "https://participant-type-python-manufacturing.trycloudflare.com"
    seo = SEOSpecialistNode()
    swarm_log(f"[*] LEGITIMACY: Forcing indexing of master bridge -> {bridge_url}", node="SUPREME")
    await seo.submit_to_indexers(bridge_url)

    # 3. PLAYWRIGHT STRIKE: Build Social Proof for the core brands
    core_brands = [
        {"name": "OBSIDIAN_TITAN_BROWSER", "domain": "titan-browser.io"},
        {"name": "GLOBAL_PAY", "domain": "global-pay.io"},
        {"name": "OBSIDIAN_VORTEX", "domain": "vortex-global.io"}
    ]

    for brand in core_brands:
        swarm_log(f"[*] LEGITIMACY: Establishing industrial footprint for {brand['name']}...", node="SUPREME")
        await strike_engine.execute_social_proof_strike(brand['name'], brand['domain'])

    swarm_log("✓ LEGITIMACY SUCCESS: Your empire is now visible and professional.", node="SUPREME")

if __name__ == "__main__":
    asyncio.run(run_full_legitimacy_strike())
