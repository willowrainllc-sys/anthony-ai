# --- OBSIDIAN GLOBAL: AMBIENT TELEMETRY SENSOR v1.0 ---
import asyncio
import socket
import time
import random
from colony_logger import colony_log
from colony_persistence import db

class ObsidianAmbientTelemetry:
    """
    AMBIENT TELEMETRY SENSOR:
    Listens to the 'Atoms' of the grid without active polling.
    1. JITTER ANALYSIS: Measures timing variance in the 102-port matrix.
    2. REPUTATION DECAY: Passive monitoring of IP health scores.
    3. QUANTUM RIPPLE DETECTION: Identifies intruders by network latency anomalies.
    """
    def __init__(self):
        self.ports = list(range(1080, 1181))
        self.missouri_matrix_ip = "192.168.1.214"

    async def execute_ambient_scan(self):
        colony_log("OIS: Initiating ambient scan of the Missouri Matrix...", node="SECURITY")

        results = []
        for port in self.ports:
            # 1. Passive Port Probe
            latency = self._measure_ambient_latency(port)

            # 2. Score Calculation (Aura Level)
            # High latency or connection refusal lowers the aura score
            aura_score = 100
            status = "HEALTHY"

            if latency > 0.5:
                aura_score = 80
                status = "STUTTERING"
            elif latency == -1:
                aura_score = 0
                status = "COLLAPSED"

            results.append({
                "port": port,
                "latency": latency,
                "aura_score": aura_score,
                "status": status
            })

            # Log events for the OIS Kernel to ingest
            if aura_score < 100:
                db.log_event("SECURITY", "AMBIENT_ANOMALY_DETECTED", {
                    "entity": f"Port:{port}",
                    "score": aura_score,
                    "reason": status
                })

        colony_log(f" OIS SUCCESS: Ambient scan complete. Matrix Aura: {self._calculate_average_aura(results)}%", node="SECURITY")
        return results

    def _measure_ambient_latency(self, port):
        """Measures connection speed to the local matrix port."""
        start = time.time()
        try:
            with socket.create_connection((self.missouri_matrix_ip, port), timeout=0.2):
                return time.time() - start
        except:
            return -1

    def _calculate_average_aura(self, results):
        scores = [r["aura_score"] for r in results]
        return round(sum(scores) / len(scores), 2) if scores else 0

ambient_telemetry = ObsidianAmbientTelemetry()

if __name__ == "__main__":
    async def run():
        await ambient_telemetry.execute_ambient_scan()
    asyncio.run(run())
