from huggingface_hub import snapshot_download
import os

# Use a flat local directory to avoid Windows symlink issues
local_dir = r"D:\AnthonyAi_Swarm\Models\LTX-Video"
os.makedirs(local_dir, exist_ok=True)

print(f"[*] Downloading LTX-Video to flat directory: {local_dir}...")
try:
    snapshot_download(
        repo_id="Lightricks/LTX-Video",
        local_dir=local_dir,
        local_dir_use_symlinks=False,
        max_workers=4
    )
    print("[✓] Download Complete!")
except Exception as e:
    print(f"[-] Download failed: {e}")
