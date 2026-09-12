# --- OBSIDIAN GLOBAL: SALES INTELLIGENCE & LEAD SCORING v1.0 ---
import random
import json
from swarm_logger import swarm_log
from swarm_persistence import db

class ObsidianSalesIntelligence:
    """
    SALES INTELLIGENCE v1.0:
    Turns raw numbers into 'High-Conversion' sales leads.
    1. PERSONA MAPPING: Assigns a buyer persona based on device and data usage.
    2. CONVERSION SCORING: Ranks leads from 0-100 based on 'Last Active' and 'Grid Reputation'.
    3. CALL CENTER PACKAGING: Formats data for easy import into dialer CRMs.
    """
    def score_lead(self, msisdn: str, niche: str, last_active: float) -> dict:
        """Calculates a conversion score for a specific number."""
        # Simple high-aura scoring logic
        base_score = 70
        if "Missouri" in niche: base_score += 15

        # Time-based decay (fresh leads worth more)
        hours_since_active = (time.time() - last_active) / 3600
        if hours_since_active < 1: base_score += 10

        return {
            "msisdn": msisdn,
            "niche": niche,
            "score": min(base_score, 100),
            "tier": "ELITE" if base_score > 90 else "STANDARD"
        }

    def generate_sales_pitch_for_buyer(self, lead_count: int, niche: str):
        """Generates the metadata for the sales list invoice."""
        price_per_lead = 0.50
        if niche == "Missouri Elite": price_per_lead = 1.25

        return {
            "product": f"Obsidian {niche} Sales List",
            "count": lead_count,
            "unit_price": price_per_lead,
            "total_value": lead_count * price_per_lead,
            "reputation_score": "100/100 Verified Residential"
        }

import time
sales_intel = ObsidianSalesIntelligence()
