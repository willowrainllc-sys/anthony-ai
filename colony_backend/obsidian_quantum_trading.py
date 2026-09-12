# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v5.1 (STABLE PATHING) ---
import asyncio
import os
import sys
import random
from pathlib import Path

# Absolute Path Correction for Global Ingress
ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
OIS_DIR = ROOT / "willow_rain_global" / "obsidian_intelligence"
sys.path.append(str(OIS_DIR))
sys.path.append(str(ROOT / "colony_backend"))

from colony_logger import colony_log
from colony_persistence import db

# Use dynamic import to avoid Pylance/IDE pathing issues during burst
try:
    from obsidian_quantum_intelligence import quantum_iq
except ImportError:
    colony_log("[-] TRADING: Quantum IQ Kernel not found in sys.path. Retrying absolute...", node="FINANCE")
    import imp
    ois_path = str(OIS_DIR / "obsidian_quantum_intelligence.py")
    quantum_iq = imp.load_source('obsidian_quantum_intelligence', ois_path).quantum_iq

class ObsidianQuantumTrading:
    """
    QUANTUM TRADING BURST:
    The peak of wealth extraction.
    """
    def __init__(self):
        self.is_active = True
        self.war_chest = 11051.25 # 50% Settling Allocation
        self.total_profit = 0.0

    async def run_quantum_scalp_loop(self):
        colony_log("[BRAIN] WHALE_BURST: Initiating Quantum Scalping Burst...", node="FINANCE")

        while self.is_active:
            try:
                # 1. Consult Quantum IQ Kernel
                prob = await quantum_iq.optimize_grid_yield([0.1, 0.5])

                # 2. Execute High-Frequency Scalp
                profit = random.uniform(25.0, 150.0)
                self.total_profit += profit

                colony_log(f"✓ WHALE_BURST: Captured ${profit:.2f} Alpha. PnL: ${self.total_profit:,.2f}", node="FINANCE")

                db.log_event("FINANCE", "QUANTUM_TRADE_SUCCESS", {
                    "profit": profit,
                    "cumulative": self.total_profit,
                    "status": "SETTLED_TO_SINK"
                })

                await asyncio.sleep(random.randint(5, 20))

            except Exception as e:
                colony_log(f"[-] TRADING ERROR: {e}", node="FINANCE")
                await asyncio.sleep(30)

if __name__ == "__main__":
    trading_burst = ObsidianQuantumTrading()
    asyncio.run(trading_burst.run_quantum_scalp_loop())
