# --- WILLOW RAIN SECURITY: OBSIDIAN GMAIL HARVESTER v1.0 (IMAP PRO) ---
import os
import sys
import re
import imapclient
import email
import httpx
import asyncio
from colony_logger import colony_log
from colony_persistence import db
from dotenv import load_dotenv

load_dotenv()

GMAIL_USER = "obsidian.global.holdings@gmail.com"
GMAIL_PASS = os.getenv("GMAIL_APP_PASSWORD")

class ObsidianGmailHarvester:
    """
    OBSIDIAN GMAIL HARVESTER v1.0:
    Direct IMAP extraction of verification signals.
    1. ZERO-BROWSER: Connects directly to Gmail servers for 100% reliability.
    2. REGEX SNIPER: Extracts 'Confirm Email' URLs from raw MIME data.
    3. AUTO-ACTIVATE: Triggers the verification handshake via hardened httpx client.
    """
    def harvest_and_verify_all(self):
        colony_log("HARVESTER: Initiating direct IMAP verification burst...", node="SECURITY")

        if not GMAIL_PASS:
            colony_log("[-] HARVESTER: No GMAIL_APP_PASSWORD found.", node="SECURITY")
            return 0

        try:
            with imapclient.IMAPClient('imap.gmail.com', use_uid=True) as client:
                client.login(GMAIL_USER, GMAIL_PASS)
                client.select_folder('INBOX')

                # Search for unread Obsidian Ingress verification emails
                messages = client.search(['UNSEEN', 'FROM', 'no-reply@obsidian_ingress.com'])
                colony_log(f"HARVESTER: Detected {len(messages)} unread verification signals.", node="SECURITY")

                verified_count = 0
                for msg_id, data in client.fetch(messages, ['RFC822']).items():
                    raw_email = data[b'RFC822'].decode('utf-8', errors='ignore')

                    # Regex to find the verification link
                    # Typically looks like: https://dashboard.obsidian_ingress.com/verify-email?token=...
                    links = re.findall(r'https://dashboard\.obsidian_ingress\.com/verify-email\?[^\s"\'<>]+', raw_email)

                    if links:
                        verify_url = links[0]
                        colony_log(f" HARVESTER: Sniped link for verify. Handshaking...", node="SECURITY")

                        # Execute the verification call
                        if self._trigger_verify_call(verify_url):
                            verified_count += 1
                            db.log_event("SECURITY", "ACCOUNT_VERIFIED_VIA_IMAP", {"url": verify_url[:50]})

                return verified_count
        except Exception as e:
            colony_log(f"[-] HARVESTER ERROR: {e}", node="SECURITY")
            return 0

    def _trigger_verify_call(self, url: str) -> bool:
        """Acts like a real browser clicking the link."""
        try:
            resp = httpx.get(url, timeout=15.0, follow_redirects=True)
            return resp.status_code == 200
        except:
            return False

gmail_harvester = ObsidianGmailHarvester()

if __name__ == "__main__":
    count = gmail_harvester.harvest_and_verify_all()
    print(f"VERIFIED_ACCOUNTS: {count}")
