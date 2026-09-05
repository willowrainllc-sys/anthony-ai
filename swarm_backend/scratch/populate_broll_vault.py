import os
import sys
import asyncio
import subprocess
from pathlib import Path

import imageio_ffmpeg
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe() or "ffmpeg"
FFMPEG_DIR = os.path.dirname(FFMPEG_EXE)

LIBRARY_DIR = Path(r"D:\AnthonyAi_Swarm\Secure_Assets\local_broll_library")
LIBRARY_DIR.mkdir(parents=True, exist_ok=True)

BROLL_SEED_QUERIES = [
    ("space_nebula.mp4", "deep space nebula cosmic 4k"),
    ("deep_ocean.mp4", "deep ocean underwater 4k"),
    ("ancient_ruins.mp4", "ancient stone ruins documentary 4k"),
    ("desert_dunes.mp4", "desert sand dunes sunset drone 4k"),
    ("cyber_matrix.mp4", "high tech server room glowing blue 4k"),
    ("mountain_wilds.mp4", "mountain peak blizzard wilderness drone 4k")
]

async def populate():
    print("=== POPULATING LOCAL 4K B-ROLL VAULT ===")
    python_exe = sys.executable

    for filename, query in BROLL_SEED_QUERIES:
        out_path = LIBRARY_DIR / filename
        if out_path.exists() and out_path.stat().st_size > 500000:
            print(f"[✓] Already exists: {filename}")
            continue

        print(f"[*] Downloading seed asset [{filename}] for query [{query}]...")
        cmd = [
            python_exe, "-m", "yt_dlp",
            "-f", "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--ffmpeg-location", FFMPEG_DIR,
            "--max-downloads", "1",
            "-o", str(out_path),
            "--quiet", "--no-warnings",
            f"ytsearch1:{query}"
        ]

        try:
            proc = await asyncio.create_subprocess_exec(*cmd)
            await asyncio.wait_for(proc.wait(), timeout=120.0)
            if out_path.exists() and out_path.stat().st_size > 500000:
                print(f"[✓] Successfully vaulted: {filename} ({out_path.stat().st_size} bytes)")
            else:
                print(f"[-] Download failed for {filename}")
        except Exception as e:
            print(f"[-] Exception downloading {filename}: {e}")

if __name__ == "__main__":
    asyncio.run(populate())
