import sys
import asyncio
import json
import os
from pathlib import Path

# Fix imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from pure_supplier_pipeline import pure_supplier_engine
from sovereign_cloud_hub import hub_master
from sovereign_syndication_engine import syndication_engine

async def get_grand_projection_v4():
    print('=== 🔱 WILLOW RAIN ENTERPRISES: GRAND REVENUE PROJECTION v4.0 ===\n')

    # 1. Pure Wholesale Upstream
    proxy_contract = await pure_supplier_engine.execute_raw_proxy_routing_supply('Geonode_Partner')
    data_contract = await pure_supplier_engine.execute_structured_data_feed_supply('OpenAI_Exchange')

    # 2. Sovereign Cloud Hub
    hub_master.lease_space_to_entity('AI-01', 'OpenAI_Data_Lab')
    hub_master.lease_space_to_entity('PX-01', 'Titan_Network_Wholesale')
    cloud_yield = await hub_master.execute_provisioning_pulse()

    # 3. Content Syndication
    syndication_engine.create_syndication_deal('Nexus_Space_Ops', 'RECURRING_SHORTS')
    syndication_engine.create_syndication_deal('Cyber_Doc_Network', 'EXCLUSIVE_LONGFORM')
    synd_yield = syndication_engine.get_total_syndication_yield()

    print('\n--- 1. PURE WHOLESALE & DATA FEED ---')
    print(f"[✓] Bulk Proxy Pipeline: ${proxy_contract.total_payout_usd:,.2f} / Cycle")
    print(f"[✓] Structured Data Feed: ${data_contract.total_payout_usd:,.2f} / Cycle")

    print('\n--- 2. SOVEREIGN CLOUD HUB (IaaS) ---')
    print(f"[✓] Active Space Rentals: ${cloud_yield:,.2f} / Month")

    print('\n--- 3. CONTENT SYNDICATION (Licensing) ---')
    print(f"[✓] White-Label Contracts: ${synd_yield:,.2f} / Month")

    grand_total = proxy_contract.total_payout_usd + data_contract.total_payout_usd + cloud_yield + synd_yield
    print(f'\n--- GRAND TOTAL PROJECTED REVENUE: ${grand_total:,.2f} / MONTH ---')

if __name__ == "__main__":
    asyncio.run(get_grand_projection_v4())
