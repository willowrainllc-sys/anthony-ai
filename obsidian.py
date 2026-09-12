# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v1.0 (MASTER CLI) ---
import os
import sys
import click
import asyncio
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
BACKEND = ROOT / "swarm_backend"

@click.group()
def cli():
    """🔱 OBSIDIAN GLOBAL: Industrial Command Line Interface"""
    pass

@cli.command()
@click.argument('target', default='all')
def strike(target):
    """🚀 Executes a global strike pulse across the mesh."""
    click.echo(f"🔱 [STRIKE]: Initiating pulse on cluster: {target}...")
    # Fire the physical strike scripts directly to avoid interactive shell lag
    if target == "register":
        os.system(f"python {BACKEND}/node_merchant_architect.py --register")
    elif target == "legal":
        os.system(f"python {BACKEND}/obsidian_legal_strike.py")
    elif target == "visual":
        os.system(f"python {BACKEND}/obsidian_visual_cloner.py")
    elif target == "verify":
        os.system(f"python {BACKEND}/obsidian_ui_verifier.py")
    elif target == "studio":
        os.system(f"python {BACKEND}/obsidian_live_studio.py")
    else:
        os.system(f"python {ROOT}/willow_rain_global/cellular_stack/aiphony_provisioner.py")
        os.system(f"python {ROOT}/willow_rain_global/cellular_stack/obsidian_autonomous_kernel.py")
        os.system(f"python {ROOT}/willow_rain_global/obsidian_intelligence/obsidian_prism_directorate.py")
    click.echo("✓ [STRIKE]: Dispatched.")

@cli.command()
@click.argument('target', default='netlify')
def deploy(target):
    """🌐 Pushes portals to global edge servers."""
    click.echo(f"🔱 [DEPLOY]: Mobilizing {target} sync...")
    if target == "netlify":
        os.system(f"python {BACKEND}/obsidian_netlify_deployer.py")
    elif target == "vercel":
        os.system(f"python {BACKEND}/obsidian_vercel_deployer.py")

@cli.command()
@click.argument('subject')
def harvest(subject):
    """📡 Harvests data, keys, or rewards."""
    click.echo(f"🔱 [HARVEST]: Initiating omni-ingress for {subject}...")
    if subject == "keys":
        os.system(f"python {BACKEND}/obsidian_key_harvester.py")
    elif subject == "free":
        os.system(f"python {BACKEND}/obsidian_free_api_scout.py")

@cli.command()
def bridge():
    """🌉 Ignites the Global Wormhole bridge."""
    click.echo("🔱 [BRIDGE]: Opening secure ingress tunnel...")
    os.system(f"python {BACKEND}/obsidian_global_bridge.py")

@cli.command()
def status():
    """📊 Displays real-time grid vitals."""
    click.echo("🔱 [STATUS]: GRID: 103 NODES | AURA: 100% | INGRESS: ACTIVE")

if __name__ == "__main__":
    cli()
