import logging
import datetime
import sys
from pathlib import Path

# --- CENTRALIZED HARDENED LOGGING ---
# Standardize all logs to the USB D: Drive
LOG_DIR = Path(r"D:\AnthonyAi_Swarm\Logs")
LOG_DIR.mkdir(exist_ok=True, parents=True)
LOG_DIR.mkdir(exist_ok=True, parents=True)
MASTER_LOG = LOG_DIR / "empire_master.log"

# Configure standard logging to file
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler(MASTER_LOG, encoding='ascii', delay=True)
    ]
)
logger = logging.getLogger("EMPIRE")

def swarm_log(message: str, node: str = "CORE"):
    """
    Principal-grade logging.
    1. Strips non-ASCII.
    2. Writes to master file.
    3. Safely attempts console output without crashing on closed handles.
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Ensure ASCII only
        clean_msg = "".join(c if ord(c) < 128 else "[*]" for c in str(message))
        formatted = f"[{timestamp}] [{node}] {clean_msg}"

        # Log to file (Always safe)
        logger.info(formatted)

        # Safe Console Output
        # We check if sys.stdout exists and is not closed
        if hasattr(sys, 'stdout') and sys.stdout is not None:
            try:
                # Direct check on closed property if it exists
                if not getattr(sys.stdout, 'closed', False):
                    sys.stdout.write(formatted + "\n")
                    sys.stdout.flush()
            except:
                pass
    except:
        pass # Never crash the caller due to logging failure

if __name__ == "__main__":
    swarm_log("Logger Test: ASCII Only. No Emojis.")
