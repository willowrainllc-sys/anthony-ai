# --- WILLOW RAIN COMPANY LLC: OBSIDIAN DIRECT-B2B PROPOSAL ENGINE v3.0 (ENTERPRISE GRADE) ---
import os
import sys
import json
import uuid
import time
import re
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
SUPPLIER_VAULT = SECURE_DIR / "pure_supplier_vault"
PROPOSAL_VAULT = SECURE_DIR / "obsidian_proposals"
PROPOSAL_VAULT.mkdir(parents=True, exist_ok=True)

# THE "RIGHT SITES": HIGH-AURA ENTERPRISE BUYERS
DIRECT_B2B_TARGETS = [
    {"name": "Bright Data", "division": "Infrastructure Partnerships", "focus": "Clean Residential Mesh"},
    {"name": "Obsidian Grid", "division": "Global IP Supply", "focus": "Enterprise Proxy Clusters"},
    {"name": "DataImpulse", "division": "Partner Network", "focus": "Mid-Tier Traffic Relay"},
    {"name": "SOAX", "division": "Infrastructure Onboarding", "focus": "Geo-Precise IP Routing"},
    {"name": "Decodo", "division": "B2B Sales", "focus": "High-Volume Data Access"},
    {"name": "OpenAI", "division": "Data Procurement", "focus": "Real-Time AI Search Indexing"},
    {"name": "Bloomberg", "division": "Financial Pipelines", "focus": "High-Freq Market Tickers"},
    {"name": "CrowdStrike", "division": "Threat Intelligence", "focus": "Global Anomaly Telemetry"}
]

class ObsidianProposalEngine:
    """
    OBSIDIAN PROPOSAL ENGINE v3.0:
    Architects high-level technical proposals for DIRECT B2B relationships.
    Bypasses consumer-level 'cash-for-ip' sites. Targets major infrastructure buyers.
    """
    def generate_handshake_proposal(self, contract_filename: str, target_idx: int = 0) -> str:
        contract_path = SUPPLIER_VAULT / contract_filename
        if not contract_path.exists():
            return f"Error: Contract {contract_filename} not found."

        with open(contract_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        target = DIRECT_B2B_TARGETS[target_idx % len(DIRECT_B2B_TARGETS)]
        proposal_id = f"SOV-{uuid.uuid4().hex[:8].upper()}"

        proposal_md = f"""
# [SUPREME] EXECUTIVE SUMMARY: Enterprise Data Infrastructure Supply
**DOCUMENT ID:** {proposal_id}
**PROVIDER:** Willow Rain Company LLC
**CLIENT:** {target['name']} ({target['division']})
**DATE:** {time.strftime('%Y-%m-%d')}

---

### 1. MISSION STATEMENT
Willow Rain Company LLC provides the world's most resilient, industrial-grade data and intelligence infrastructure. Our mission is to empower {target['name']} with high-fidelity, unflagged network ingress and structured data streams designed specifically for enterprise-scale AI and security operations.

### 2. CORE INFRASTRUCTURE SPECIFICATIONS
- **DECENTRALIZED MATRIX:** Distributed 16-Port residential gateway matrix with multi-region cloud failover.
- **THROUGHPUT CAPACITY:** {data.get('allocated_bandwidth_tb', 0.0):,.2f} Terabytes per cycle burst capacity.
- **ELITE REPUTATION:** Guaranteed 100/100 ISP-grade reputation score on all exit nodes.
- **LOW-LATENCY EDGE:** Average round-trip latency of <18ms to major financial and data hubs.

### 3. DATA INTEGRITY & COMPLIANCE
- **DIGITAL PROVENANCE:** Every data packet and refined record is hashed with SHA-256 for legal-grade chain of custody.
- **SLA GUARANTEE:** We provide a 99.99% uptime Service Level Agreement (SLA).
- **ETHICAL SOURCING:** All data is sourced via informed, opt-in peer participation.

### 4. COMMERCIAL TERMS
- **MONTHLY RETAINER:** ${data.get('total_payout_usd', 0.0):,.2f} USD
- **SETTLEMENT ROUTE:** Direct ACH Bank Wire (Willow Rain Company LLC) or Secured Stablecoin Ingress.
- **CONTRACT PERIOD:** 12-Month Service Agreement with monthly milestone reviews.

### 5. CONNECTION ENDPOINT (SECURE)
`{data.get('vendor_api_endpoint', 'socks5://willow_rain:token@47.85.50.46:8000')}`

---

### 6. AUTHORIZATION
I, **Obsidian Christopher Maestas**, Director of Willow Rain Company LLC, certify that our infrastructure meets the highest standards of the Fortune 500.

**SIGNATURE:**
*Obsidian Christopher*
Director, Willow Rain Company LLC
        """

        out_file = PROPOSAL_VAULT / f"proposal_{target['name'].replace(' ', '_')}_{proposal_id}.md"
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(proposal_md)

        db.log_event("PROPOSAL", "ENTERPRISE_B2B_PROPOSAL_GENERATED", {
            "proposal_id": proposal_id,
            "target": target['name'],
            "value": data.get('total_payout_usd', 0.0),
            "vault_path": str(out_file)
        })

        swarm_log(f" PROPOSAL SUCCESS: Direct B2B Handshake [{proposal_id}] generated for {target['name']}!", node="PROPOSAL")
        return proposal_md

proposal_engine = ObsidianProposalEngine()

if __name__ == "__main__":
    contracts = sorted(list(SUPPLIER_VAULT.glob("contract_proxy_*.json")), key=os.path.getmtime, reverse=True)
    if contracts:
        proposal = proposal_engine.generate_handshake_proposal(contracts[0].name, target_idx=0) # Target Bright Data
        print(f"DIRECT B2B PROPOSAL GENERATED FOR: Bright Data")
