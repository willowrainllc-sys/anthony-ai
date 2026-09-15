# --- Owned by Anthony Christopher Maestas | Directed by ARES ---
# --- ARES GUARDIAN WATCH: PHYSICAL MONITORING & PROTECTION v1.0 ---
import asyncio
import os
import time
import httpx
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db
from obsidian_emergency_notifier import emergency_notifier

class AresGuardianWatch:
    """
    ARES GUARDIAN WATCH:
    1. PHYSICAL HEARTBEAT: Monitors for the Director's primary node pulse (HUD/Phone).
    2. ORACLE ANALYSIS: Uses LLM to analyze 'Anomaly Status' and determine risk level.
    3. ESCALATION: Automatically triggers failover alerts and emergency notifications.
    """
    def __init__(self):
        self.boss = "Anthony Maestas"
        self.oracle_key = os.getenv("OPENROUTER_API_KEY")
        self.last_seen = time.time()
        self.protection_active = True

    async def check_director_presence(self):
        """Monitors for the Director's secure link pulse."""
        while self.protection_active:
            # [+] Simulation: Checking for encrypted handshake from primary mobile node
            # In a real scenario, this would be a socket or database check
            current_time = time.time()
            gap = current_time - self.last_seen

            if gap > 300: # 5 minutes of silence
                colony_log(f"[!] ARES_GUARDIAN: Director {self.boss} silence detected. Analyzing risk...", node="SECURITY")
                await self.escalate_to_oracle()

            await asyncio.sleep(60)

    async def escalate_to_oracle(self):
        """Consults the Oracle to determine if an emergency alert is required."""
        prompt = f"ARES GUARDIAN Alert: Director {self.boss} has not pulsed in 300 seconds. Review global mesh status and decide if we should trigger failover protocols. Respond with ACTION: [ALERT|MONITOR]."

        headers = {"Authorization": f"Bearer {self.oracle_key}", "Content-Type": "application/json"}
        payload = {
            "model": "google/gemini-flash-1.5",
            "messages": [{"role": "system", "content": "You are the Obsidian Guardian Oracle."},
                         {"role": "user", "content": prompt}]
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers)
                if resp.status_code == 200:
                    action = resp.json()['choices'][0]['message']['content']
                    if "ALERT" in action.upper():
                        colony_log("[+] ORACLE COMMAND: TRIGGERING EMERGENCY NOTIFICATION.", node="SECURITY")
                        emergency_notifier.send_failover_alert("ARES_SECURE_NODE_01", 8080)
                    else:
                        colony_log("ARES_GUARDIAN: Oracle recommends monitoring. No alert sent.", node="SECURITY")
        except Exception as e:
            colony_log(f"[-] GUARDIAN ORACLE ERROR: {e}", node="SECURITY")

if __name__ == "__main__":
    guardian = AresGuardianWatch()
    asyncio.run(guardian.check_director_presence())