# --- WILLOW RAIN SECURITY: OBSIDIAN EMERGENCY NOTIFIER & FAILOVER HUB v1.0 ---
import os
import smtplib
import time
from email.mime.text import MIMEText
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

# GMAIL CONFIGURATION
GMAIL_USER = "obsidian.global.holdings@gmail.com"
GMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD") # Required for automated sending

class ObsidianEmergencyNotifier:
    """
    EMERGENCY NOTIFIER v1.0:
    The "Grid-Dead" Alert System.
    1. FAILOVER PUSH: Sends new port/IP info to Obsidian if the primary drops.
    2. COMMAND DISPATCH: Includes the 'Command Text' needed to re-link the phone/HUD.
    3. HEARTBEAT: Confirms the 2nd Base (Cloud Mirror) is active and saving money.
    """
    def send_failover_alert(self, new_ip: str, new_port: int):
        colony_log(f" EMERGENCY: Sending failover alert to Director Maestas...", node="SECURITY")

        if not GMAIL_PASS:
            colony_log("[-] ALERT FAIL: No GMAIL_APP_PASSWORD found in .env.", node="SECURITY")
            return False

        subject = "[SUPREME] WILLOW RAIN SECURITY: GRID FAILOVER ACTIVATED"
        command_text = f"python colony_backend/obsidian_production_launcher.py --remote {new_ip}:{new_port}"

        body = f"""
        Director Obsidian Christopher,

        CRITICAL: The Primary Grid at 127.0.0.1 has disconnected.
        The OBSIDIAN PERSISTENCE engine has successfully activated the 2nd Base (Cloud Mirror).

        The money machine is LIVE and SAVING CAPITAL in SAFE_MODE.

        --- NEW LOGIN DATA ---
        IP:   {new_ip}
        PORT: {new_port}
        STATUS: COLLECTING_ONLY (Safe Mode)

        --- HUD RE-LINK COMMAND ---
        {command_text}

        The grid is unbreakable. Focus on the Chief Aim.

        Regards,
        Obsidian Daemon Core
        """

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = GMAIL_USER
        msg['To'] = GMAIL_USER

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(GMAIL_USER, GMAIL_PASS)
                server.send_message(msg)
            colony_log(" EMERGENCY: Failover alert dispatched to Gmail.", node="SECURITY")
            return True
        except Exception as e:
            colony_log(f"[-] ALERT ERROR: {e}", node="SECURITY")
            return False

emergency_notifier = ObsidianEmergencyNotifier()

if __name__ == "__main__":
    # Test alert
    emergency_notifier.send_failover_alert("47.85.50.46", 8000)
