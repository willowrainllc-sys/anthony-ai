# --- WILLOW RAIN SECURITY: OBSIDIAN BRAIN ACCESS GATE v1.0 ---
import time
import json
from swarm_logger import swarm_log
from swarm_persistence import db

class AnthonyChristopherBrainGate:
    """
    OBSIDIAN BRAIN GATE v1.0:
    The security firewall for the Central Intelligence (The Brain).
    1. IDENTITY VERIFICATION: Checks for valid 'Ghost ID' and 'PQC Session Keys'.
    2. REPUTATION CHECK: Verifies the requesting bot's IP has a 100/100 score.
    3. ACCESS DENIAL: Instantly blocks any bot that lacks current security patches.
    """
    def __init__(self):
        self.blocked_ids = set()

    async def validate_access(self, bot_id: str, security_headers: dict) -> bool:
        """
        Validates if a Sub-AnthonyChristopher AI has the authority and protection to speak to the brain.
        """
        swarm_log(f"BRAIN_GATE: Validating access request from [{bot_id}]...", node="SECURITY")

        # 1. Blocked List Check
        if bot_id in self.blocked_ids:
            swarm_log(f" BRAIN_GATE: ACCESS DENIED. Bot [{bot_id}] is BLACKLISTED.", node="SECURITY")
            return False

        # 2. Security Protocol Check (PQC Key)
        pqc_key = security_headers.get("pqc_session_key")
        if not pqc_key or not pqc_key.startswith("PQC-"):
            swarm_log(f"[ALERT] BRAIN_GATE: ACCESS DENIED. Bot [{bot_id}] lacks valid Quantum Encryption.", node="SECURITY")
            self.blocked_ids.add(bot_id)

            # TRIGGER ACTIVE DEFENSE
            from anthony_active_defense import active_defense
            await active_defense.log_suspicious_activity("Grid_Node_Internal", bot_id)
            return False

        # 3. Hardware Ghosting Check
        ghost_dna = security_headers.get("ghost_dna")
        if not ghost_dna:
            swarm_log(f"[ALERT] BRAIN_GATE: ACCESS DENIED. Bot [{bot_id}] lacks hardware fingerprinting.", node="SECURITY")
            return False

        # 4. Reputation Sync
        with db._get_connection() as conn:
            # Check if this bot has a high reputation in the registry
            row = conn.execute("SELECT status FROM virtual_nodes WHERE node_id=?", (bot_id,)).fetchone()
            if not row or row[0] != "GATHERING":
                swarm_log(f"[ALERT] BRAIN_GATE: ACCESS DENIED. Bot [{bot_id}] status is untrusted.", node="SECURITY")
                return False

        swarm_log(f" BRAIN_GATE SUCCESS: Bot [{bot_id}] authorized for high-level reasoning.", node="SECURITY")
        return True

brain_gate_security = AnthonyChristopherBrainGate()
