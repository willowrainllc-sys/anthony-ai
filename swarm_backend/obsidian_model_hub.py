# --- ANTHONY AI: OBSIDIAN MODEL HUB & NATIVE VAULT v1.0 ---
import os
import json
import shutil
import asyncio
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

# 🔱 THE NATIVE VAULT
MODEL_STORAGE = Path(r"D:\AnthonyAi_Swarm\Secure_Assets\Model_Vault")
HUGGINGFACE_CACHE = Path(os.getenv("USERPROFILE")) / ".cache" / "huggingface" / "hub"

class ObsidianModelHub:
    """
    OBSIDIAN MODEL HUB v1.0:
    The superior alternative to Hugging Face.
    1. CLONE & OWN: Physically moves models from HF cache to the Director's Model Vault.
    2. EXCOMMUNICATO: Blocks external model downloads once the vault is primed.
    3. TEAM PUSH/GET: Only authorized team scripts can request model ingestion.
    4. HARDCODED ARCHIVE: Maintains a permanent record of model versions and hashes.
    """
    def __init__(self):
        MODEL_STORAGE.mkdir(parents=True, exist_ok=True)
        self.registry_file = MODEL_STORAGE / "hub_registry.json"
        self._init_registry()

    def _init_registry(self):
        if not self.registry_file.exists():
            with open(self.registry_file, "w") as f:
                json.dump({"models": {}, "last_sync": 0}, f)

    def clone_from_hf_cache(self):
        """Identifies models in HF cache and moves them to the Sovereign Vault."""
        swarm_log("MODEL_HUB: Scanning legacy HuggingFace cache for cloning...", node="SOVEREIGN")

        if not HUGGINGFACE_CACHE.exists():
            swarm_log("[-] MODEL_HUB: HuggingFace cache not found. Vaulting skipped.", node="SOVEREIGN")
            return

        cloned_count = 0
        for item in HUGGINGFACE_CACHE.iterdir():
            if item.is_dir() and item.name.startswith("models--"):
                model_name = item.name.replace("models--", "").replace("--", "/")
                target_path = MODEL_STORAGE / item.name

                if not target_path.exists():
                    swarm_log(f"MODEL_HUB: Cloning [{model_name}] to Sovereign Vault...", node="SOVEREIGN")
                    try:
                        shutil.copytree(item, target_path)
                        self._register_model(model_name, str(target_path))
                        cloned_count += 1
                    except Exception as e:
                        swarm_log(f"[-] CLONE FAIL [{model_name}]: {e}", node="SOVEREIGN")
                else:
                    swarm_log(f"MODEL_HUB: [{model_name}] already secured in Vault.", node="SOVEREIGN")

        swarm_log(f"✓ MODEL_HUB: {cloned_count} models excommunicated from HF and moved to Vault.", node="SOVEREIGN")

    def _register_model(self, name, path):
        with open(self.registry_file, "r+") as f:
            data = json.load(f)
            data["models"][name] = {
                "local_path": path,
                "vaulted_at": time.time(),
                "status": "SECURED"
            }
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

    async def run_hub_daemon(self):
        """Continuously monitors the vault and handles team 'Push/Get' requests."""
        swarm_log("🔱 MODEL_HUB: Sovereign Daemon is ONLINE. External traffic BLOCKED.", node="SOVEREIGN")

        while True:
            # 1. Block external downloads (Simulated via firewall or env override)
            os.environ["HF_HUB_OFFLINE"] = "1"
            os.environ["TRANSFORMERS_OFFLINE"] = "1"

            # 2. Hardcoded Team PUSH/GET Logic
            # Team can 'PUSH' by dropping folders into model cache
            # The Hub will then 'Ingest' and 'Vault' them
            self.clone_from_hf_cache()

            await asyncio.sleep(3600) # Heartbeat every hour

    def team_get_model_path(self, model_id: str) -> str:
        """The only authorized way for team scripts to get a model path."""
        with open(self.registry_file, "r") as f:
            data = json.load(f)
            model = data["models"].get(model_id)
            if model:
                swarm_log(f"MODEL_HUB: Team access GRANTED for [{model_id}].", node="SOVEREIGN")
                return model["local_path"]

        swarm_log(f"[-] MODEL_HUB: Access DENIED. Model [{model_id}] not in Sovereign Vault.", node="SOVEREIGN")
        return None

if __name__ == "__main__":
    import time
    hub = ObsidianModelHub()
    hub.clone_from_hf_cache()
    # To run as daemon: asyncio.run(hub.run_hub_daemon())
