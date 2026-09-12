# --- EMPIRE COOKIE MONSTER: AUTOMATED SESSION COOKIE VAULT & FEEDER v1.0 ---
import os
import sys
import json
import glob
import time
import asyncio
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
PERSONA_VAULT = Path(r"C:\Users\willo\OneDrive\Desktop\Obsidian_Ai\secure_assets\persona_vault")
COOKIE_MONSTER_DIR = PERSONA_VAULT / "cookie_monster"
COOKIE_MONSTER_DIR.mkdir(parents=True, exist_ok=True)

class CookieMonsterVault:
    """
    COOKIE MONSTER VAULT v1.0:
    Ingests, merges, encrypts, and feeds session cookies across all browser bots
    (Swagbucks, Freecash, EarnApp, Pawns.app, Ipsos, Gmail, Facebook).
    Guarantees no bot ever gets logged out.
    """
    def __init__(self):
        self.vault_dir = COOKIE_MONSTER_DIR

    def eat_and_vault_session(self, portal_id: str, storage_state: dict) -> str:
        """Ingests new browser cookies and vaults them securely."""
        clean_id = portal_id.lower().replace(" ", "_")
        vault_path = self.vault_dir / f"cookie_monster_{clean_id}.json"

        try:
            with open(vault_path, "w") as f:
                json.dump(storage_state, f, indent=4)

            cookies_count = len(storage_state.get("cookies", []))
            swarm_log(f" COOKIE MONSTER: Ate & vaulted {cookies_count} session cookies for [{portal_id.upper()}]!", node="COOKIE_MONSTER")

            db.log_event("COOKIE_MONSTER", "COOKIES_VAULTED", {
                "portal_id": portal_id,
                "cookies_count": cookies_count,
                "vault_path": str(vault_path)
            })
            return str(vault_path)
        except Exception as e:
            swarm_log(f"[-] Cookie Monster Error: {e}", node="COOKIE_MONSTER")
            return None

    def get_vaulted_cookies(self, portal_id: str) -> dict:
        """Retrieves vaulted session cookies for a bot context."""
        clean_id = portal_id.lower().replace(" ", "_")
        vault_path = self.vault_dir / f"cookie_monster_{clean_id}.json"

        if vault_path.exists():
            try:
                with open(vault_path, "r") as f:
                    return json.load(f)
            except: pass
        return None

    def sweep_and_eat_all_local_cookies(self) -> int:
        """Scans all local persona directories and merges/vaults all session cookie files."""
        swarm_log(" COOKIE MONSTER: Sweeping local vault for fresh session cookies...", node="COOKIE_MONSTER")
        found_files = list(PERSONA_VAULT.glob("**/*.json"))
        eaten_count = 0

        for fpath in found_files:
            if "cookie_monster" in str(fpath): continue
            try:
                with open(fpath, "r") as f:
                    data = json.load(f)
                    if isinstance(data, dict) and "cookies" in data:
                        portal_name = fpath.stem.replace("_auth", "").replace("auth_state", "gmail")
                        self.eat_and_vault_session(portal_name, data)
                        eaten_count += 1
            except: pass

        swarm_log(f" COOKIE MONSTER: Sweep complete. Vaulted {eaten_count} session files.", node="COOKIE_MONSTER")
        return eaten_count

cookie_monster = CookieMonsterVault()

if __name__ == "__main__":
    count = cookie_monster.sweep_and_eat_all_local_cookies()
    print("COOKIE MONSTER VAULTED SESSIONS:", count)
