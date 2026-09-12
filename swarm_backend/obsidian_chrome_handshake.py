# --- WILLOW RAIN SECURITY: OBSIDIAN CHROME HANDSHAKE v1.0 ---
import os
import subprocess
import sys
from pathlib import Path

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
USER_DATA = r"C:\Users\willo\AppData\Local\Google\Chrome\User Data"

def open_live_handshake(portal_url: str):
    """
    Opens your REAL Chrome browser to the portal.
    This allows you to log in with your saved cookies and 2FA.
    The AI will then 'Snipe' the resulting session.
    """
    print(f"[SUPREME] CHROME_HANDSHAKE: Opening live portal -> {portal_url}")

    # Command to open Chrome with your specific user data profile
    # This ensures your saved passwords and sessions are visible
    cmd = f'"{CHROME_PATH}" --user-data-dir="{USER_DATA}" --profile-directory="Default" "{portal_url}"'

    try:
        subprocess.Popen(cmd, shell=True)
        print("\n[!] ACTION REQUIRED: Log in to the account that says $0.06.")
        print("[!] Once the correct dashboard is visible, return here.")
    except Exception as e:
        print(f"[-] Error opening Chrome: {e}")

if __name__ == "__main__":
    # Target the login page to ensure we capture fresh keys
    open_live_handshake("https://dashboard.obsidian_ingress.com/login")
