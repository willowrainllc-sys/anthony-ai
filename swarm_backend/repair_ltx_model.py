# --- EMPIRE LTX REPAIR: FORCE WEIGHT SYNCHRONIZATION v1.0 ---
import os
import torch
from diffusers import LTXPipeline
from swarm_logger import swarm_log
from pathlib import Path

def repair_ltx():
    swarm_log("REPAIR: Forcing full LTX-Video weight synchronization...", node="LTX")

    local_dir = r"D:\AnthonyAi_Swarm\Models\LTX-Video"
    os.makedirs(local_dir, exist_ok=True)

    try:
        from huggingface_hub import snapshot_download
        swarm_log(f"REPAIR: Synchronizing to {local_dir}...", node="LTX")

        snapshot_download(
            repo_id="Lightricks/LTX-Video",
            local_dir=local_dir,
            local_dir_use_symlinks=False,
            max_workers=4
        )

        swarm_log("[✓] REPAIR SUCCESS: LTX-Video model is fully synchronized.", node="LTX")
        return True
    except Exception as e:
        swarm_log(f"[-] REPAIR FAIL: {e}", node="LTX")
        return False
    except Exception as e:
        swarm_log(f"[-] REPAIR FAIL: {e}", node="LTX")
        return False

if __name__ == "__main__":
    repair_ltx()
