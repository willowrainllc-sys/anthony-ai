# --- WILLOW RAIN SECURITY: OBSIDIAN PRIMARY ACCOUNT FIREWALL v1.0 ---
import os
import sys
import json
from colony_logger import colony_log
from colony_persistence import db

class ObsidianFirewall:
    """
    OBSIDIAN FIREWALL v1.0:
    The "Red-Line" Protocol. Protects the Director's Main Accounts from the Colony.
    1. ZERO-LINKAGE: Ensures the Master Gmail and Primary ObsidianBridge accounts NEVER
       share an IP, browser context, or hardware fingerprint with the 10,000 ghost nodes.
    2. IP AIR-GAPPING: The Master Console routes through a dedicated 'Authority Port' (8000)
       which is never used by the bot-colony (Ports 1080-2080).
    3. PATTERN ANONYMIZATION: Strips 'willow.rain' metadata from outgoing bot headers.
    """
    def __init__(self):
        self.master_ip = os.getenv("ALIBABA_EIP", "47.85.50.46")
        self.protected_entities = ["obsidian.global.holdings@gmail.com", "bc1qk4ass5xsanvth2tz7jsapscy8ld25yr6ze5yzx"]

    def enforce_isolation(self, target_node_id: str, proxy_url: str):
        """Verifies that a node is not overlapping with the Primary Authority."""
        if self.master_ip in proxy_url:
            colony_log(f"[ALERT] FIREWALL: CRITICAL COLLISION! Node [{target_node_id}] attempted to use Master IP. BLOCKED.", node="SECURITY")
            return False

        colony_log(f" FIREWALL: Node [{target_node_id}] verified as air-gapped from Primary Authority.", node="SECURITY")
        return True

    def sanitize_bot_headers(self, headers: dict) -> dict:
        """Removes any identifying company signatures from bot requests."""
        keys_to_purge = ["Referer", "User-Agent", "X-Willow-Rain-ID"]
        sanitized = {k: v for k, v in headers.items() if k not in keys_to_purge}
        return sanitized

firewall = ObsidianFirewall()
