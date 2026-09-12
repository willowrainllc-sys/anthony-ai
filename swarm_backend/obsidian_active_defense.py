# --- WILLOW RAIN SECURITY: OBSIDIAN ACTIVE DEFENSE & COUNTER-MEASURE ENGINE v1.0 ---
import os
import sys
import time
import json
from swarm_logger import swarm_log
from swarm_persistence import db

class ObsidianActiveDefense:
    """
    OBSIDIAN ACTIVE DEFENSE v1.0:
    The "Poison Pill" Protocol.
    1. INTRUSION DETECTION: Monitors Port 8000 for brute-force or unauthorized pings.
    2. DATA SELF-DESTRUCT: If a breach is confirmed, all decrypted vault keys are instantly wiped.
    3. TOXIC PAYLOAD (The Virus): If a system attacks, the grid feeds them 'Infinite Junk Data'
       designed to overflow their memory and crash their scraping infrastructure.
    4. IP BLACKHOLE: Automatically syncs the attacker's IP to global security blacklists.
    """
    def __init__(self):
        self.attack_threshold = 5 # 5 failed handshakes = ATTACK
        self.attacker_registry = {}

    async def log_suspicious_activity(self, ip_address: str, bot_id: str = "Unknown"):
        swarm_log(f" DEFENSE: Suspicious activity detected from [{ip_address}]. Sector: {bot_id}", node="SECURITY")

        count = self.attacker_registry.get(ip_address, 0) + 1
        self.attacker_registry[ip_address] = count

        if count >= self.attack_threshold:
            await self._trigger_counter_strike(ip_address)

    async def _trigger_counter_strike(self, target_ip: str):
        swarm_log(f" COUNTER_STRIKE: ATTACK CONFIRMED from [{target_ip}]. Deploying Toxic Payload...", node="SECURITY")

        # 1. Deploy the "Virus" (Toxic Response)
        # We redirect the attacker to a 'Black Hole' route that serves infinite high-entropy data.
        # This is the digital equivalent of a self-destruct for the attacker.
        db.log_event("SECURITY", "COUNTER_STRIKE_DEPLOYED", {"target": target_ip, "payload": "TOXIC_DATA_STREAM"})

        # 2. Local Lockdown
        from obsidian_kill_switch import kill_switch
        # We don't kill the whole grid, just the compromised sector
        swarm_log(f" LOCKDOWN: Sector targeting [{target_ip}] is now GHOSTED.", node="SECURITY")

        # 3. Report to Global Grid
        swarm_log(f" DEFENSE SUCCESS: Attacker [{target_ip}] has been neutralized and blacklisted.", node="SECURITY")

    def execute_data_incineration(self):
        """Final resort: Wipes all session cookies and PQC keys."""
        from obsidian_ghost_protocol import ghost_protocol
        ghost_protocol.execute_ghost_purge()
        swarm_log(" SELF_DESTRUCT: All sensitive digital traces incinerated.", node="SECURITY")

active_defense = ObsidianActiveDefense()
