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
from sovereign_compute_renter import compute_renter
from sovereign_lead_generator import lead_gen
from ai_ad_creative_agency import ad_agency
from wholesale_market_explorer import market_explorer

async def get_grand_projection_v6():
    print('=== 🔱 WILLOW RAIN ENTERPRISES: GRAND REVENUE PROJECTION v6.0 ===\n')

    # 1. Pure Wholesale Upstream
    proxy_contract = await pure_supplier_engine.execute_raw_proxy_routing_supply('Geonode_Partner')
    data_contract = await pure_supplier_engine.execute_structured_data_feed_supply('OpenAI_Exchange')

    # 2. Sovereign Cloud Hub
    hub_master.lease_space_to_entity('AI-01', 'OpenAI_Data_Lab')
    cloud_yield = await hub_master.execute_provisioning_pulse()

    # 3. Content Syndication
    synd_yield = syndication_engine.get_total_syndication_yield()

    # 4. Sovereign Compute & GPU Rental
    compute_manifest = compute_renter.generate_compute_manifest()

    # 5. B2B Lead Generation
    lead_package = await lead_gen.harvest_high_intent_leads("Real Estate")

    # 6. AI AD CREATIVE AGENCY (NEW)
    ad_pkg = await ad_agency.create_wholesale_ad_package("Luxury Brands Group", goal="CONVERSION", count=10)

    # 7. UNTAPPED WHOLESALE MARKETS (NEW)
    # Using the report total
    market_report_raw = market_explorer.generate_market_report()
    market_report = json.loads(market_report_raw)
    untapped_yield = market_report["combined_projected_yield"]

    print('\n--- 1. PURE WHOLESALE & DATA FEED ---')
    print(f"[✓] Bulk Proxy Pipeline: ${proxy_contract.total_payout_usd:,.2f} / Cycle")
    print(f"[✓] Structured Data Feed: ${data_contract.total_payout_usd:,.2f} / Cycle")

    print('\n--- 2. SOVEREIGN CLOUD & COMPUTE (IaaS) ---')
    print(f"[✓] Active Space Rentals: ${cloud_yield:,.2f} / Month")
    print(f"[✓] GPU/CPU Compute Yield: ${compute_manifest.estimated_monthly_gross_usd:,.2f} / Month")

    print('\n--- 3. DATA & LEAD ARBITRAGE ---')
    print(f"[✓] B2B Lead Generation: ${lead_package.wholesale_price_usd:,.2f} / Package")

    print('\n--- 4. CONTENT SYNDICATION & AD AGENCY ---')
    print(f"[✓] White-Label Deals: ${synd_yield:,.2f} / Month")
    print(f"[✓] Ad Creative Agency: ${ad_pkg.wholesale_price_usd:,.2f} / Package")

    print('\n--- 5. UNTAPPED WHOLESALE OPPORTUNITIES ---')
    print(f"[✓] Market Scaling Capacity: ${untapped_yield:,.2f} / Month")

    grand_total = (proxy_contract.total_payout_usd +
                   data_contract.total_payout_usd +
                   cloud_yield +
                   compute_manifest.estimated_monthly_gross_usd +
                   lead_package.wholesale_price_usd +
                   synd_yield +
                   ad_pkg.wholesale_price_usd +
                   untapped_yield)

    print(f'\n--- GRAND TOTAL PROJECTED REVENUE: ${grand_total:,.2f} / MONTH ---')

if __name__ == "__main__":
    asyncio.run(get_grand_projection_v6())
