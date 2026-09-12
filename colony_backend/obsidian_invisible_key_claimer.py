# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v1.0 (INVISIBLE KEY CLAIMER) ---
import json
import re
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

ROOT = Path(r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai")
VAULT_PATH = ROOT / "secure_assets" / "industrial_api_vault.json"

class InvisibleKeyClaimer:
    """
    INVISIBLE KEY CLAIMER:
    Scours the internal codebase for hardcoded signatures and 'ghost' credentials.
    1. MANIFEST HARVEST: Extracts AR and Mesh keys from Android source.
    2. PROMO SNIPE: Captures internal coupon codes and reward signatures.
    3. AUTH AGGREGATOR: Pulls session tokens from persona vaults.
    4. VAULT CONSOLIDATION: Merges all 'Invisible' findings into the Industrial Vault.
    """
    def __init__(self):
        self.findings = {}

    def claim_invisible_keys(self):
        colony_log("CLAIMER: Initiating Deep Code Scour for invisible signatures...", node="SECURITY")

        # 🔱 1. Android Manifest AR Key
        manifest_path = ROOT / "app" / "src" / "main" / "AndroidManifest.xml"
        if manifest_path.exists():
            content = manifest_path.read_text()
            match = re.search(r'vps\.apiKey" android:value="([^"]+)"', content)
            if match:
                self.findings["GOOGLE_AR_CORE"] = match.group(1)
                colony_log("✓ CLAIMER: Google AR_VPS Key acquired from Manifest.", node="SECURITY")

        # 🔱 2. Mesh Internal Auth Key
        mesh_api_path = ROOT / "app" / "src" / "main" / "java" / "com" / "obsidian" / "global" / "MeshApiService.kt"
        if mesh_api_path.exists():
            content = mesh_api_path.read_text()
            match = re.search(r'OBSIDIAN_API_KEY = "([^"]+)"', content)
            if match:
                self.findings["MESH_INTERNAL_AUTH"] = match.group(1)
                colony_log("✓ CLAIMER: Mesh Internal Signature acquired.", node="SECURITY")

        # 🔱 3. Promo Codes
        factory_path = ROOT / "colony_backend" / "obsidian_account_factory.py"
        if factory_path.exists():
            content = factory_path.read_text()
            match = re.search(r'COUPON_CODE = "([^"]+)"', content)
            if match:
                self.findings["SIGNUP_PROMO_CODE"] = match.group(1)
                colony_log(f"✓ CLAIMER: Ghost Promo Code [{match.group(1)}] acquired.", node="SECURITY")

        # 🔱 4. Vercel Project DNA
        env_path = ROOT / ".env"
        if env_path.exists():
            content = env_path.read_text()
            url_match = re.search(r'VERCEL_URL=(.+)', content)
            if url_match:
                self.findings["VERCEL_PRODUCTION_ENDPOINT"] = url_match.group(1).strip()

        # 🔱 5. Session Token Scavenge (Ghost Vault)
        persona_vault = ROOT / "secure_assets" / "persona_vault" / "game_sessions"
        if persona_vault.exists():
            for auth_file in persona_vault.glob("*.json"):
                try:
                    raw_content = auth_file.read_text()
                    # 🔱 ULTRA-AGGRESSIVE: Match labels even with escaped quotes
                    tokens = re.findall(r'\\?"[a-zA-Z0-9_-]*(?:token|key|secret|auth|sid)\\?":\s*\\?"([^\\"]+)\\?"', raw_content, re.IGNORECASE)

                    # 🔱 Look for raw JWTs (starts with eyJ)
                    jwts = re.findall(r'eyJ[a-zA-Z0-9_-]+\.eyJ[a-zA-Z0-9_-]+\.[a-zA-Z0-9_-]+', raw_content)

                    all_found = list(set(tokens + jwts))
                    count = 0
                    for i, t in enumerate(all_found):
                        if len(t) > 15:
                            self.findings[f"GHOST_SIG_{auth_file.stem.upper()}_{i}"] = t
                            count += 1

                    colony_log(f"✓ CLAIMER: {count} signatures acquired from {auth_file.name}.", node="SECURITY")
                except: pass

        self._sync_to_vault()

    def _sync_to_vault(self):
        if not VAULT_PATH.exists():
            colony_log("[-] CLAIMER: Industrial Vault not found. Creating new instance.", node="SECURITY")
            vault = {"active_vault": {"INVISIBLE_KEYS": {}}}
        else:
            with open(VAULT_PATH, 'r') as f:
                vault = json.load(f)

        if "INVISIBLE_KEYS" not in vault["active_vault"]:
            vault["active_vault"]["INVISIBLE_KEYS"] = {}

        vault["active_vault"]["INVISIBLE_KEYS"].update(self.findings)

        with open(VAULT_PATH, 'w') as f:
            json.dump(vault, f, indent=4)

        colony_log(f"✓ CLAIMER SUCCESS: {len(self.findings)} invisible keys consolidated in Vault.", node="SECURITY")
        db.log_event("SECURITY", "INVISIBLE_KEYS_CLAIMED", {"count": len(self.findings)})

if __name__ == "__main__":
    claimer = InvisibleKeyClaimer()
    claimer.claim_invisible_keys()
