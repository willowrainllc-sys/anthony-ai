# --- WILLOW RAIN APP CORE MCP SERVER v4.0 (GOD-MODE ASYNC) ---
import os
import sys
import json
import asyncio
from pathlib import Path
from fastmcp import FastMCP
from dotenv import load_dotenv

sys.path.append(os.path.dirname(__name__))

from swarm_logger import swarm_log
from swarm_persistence import db

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

mcp = FastMCP("WillowRain App Core MCP")

@mcp.tool()
async def query_app_database(table_name: str, limit: int = 5) -> list:
    try:
        with db._get_connection() as conn:
            cur = conn.cursor()
            rows = cur.execute(f"SELECT * FROM {table_name} LIMIT ?", (limit,)).fetchall()
            col_names = [description[0] for description in cur.description]
            return [dict(zip(col_names, r)) for r in rows]
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
async def trigger_longform_strike(publish_live: bool = False) -> dict:
    from longform_production_orchestrator import longform_orchestrator
    return await longform_orchestrator.execute_longform_strike(publish_live=publish_live)

@mcp.tool()
async def trigger_master_strike(category: str = "exoplanetary_anomalies", target_min: int = 1) -> dict:
    from master_studio import master_factory
    return await master_factory.produce_and_dispatch_episode(
        channel_id="ANTHONY_AI_OFFICIAL",
        category=category,
        ep_num=1,
        target_min=target_min,
        content_type="SHORT_FORM" if target_min <= 3 else "LONG_FORM"
    )

@mcp.tool()
async def audit_obsidian_ingress_data_flows() -> dict:
    from obsidian_ingress_data_flow_auditor import flow_auditor
    return await flow_auditor.audit_all_flows()

@mcp.tool()
async def trigger_100x_data_flow_scaling(service_id: str = "OBSIDIAN_INGRESS") -> dict:
    from mass_account_onboarder import account_onboarder
    from obsidian_node_multiplexer import node_multiplexer
    # 1. Provision 100 unique IP nodes
    await node_multiplexer.provision_100_node_physical_cluster(service_id)
    # 2. Run the onboarding blitz
    count = await account_onboarder.run_god_mode_blitz(service_id)
    return {"status": "SUCCESS", "accounts_synchronized": count, "total_target": 100}

@mcp.tool()
async def trigger_mastermind_trade_strike() -> dict:
    """
    Executes a high-conviction trade strike using the Trading Mastermind Team.
    Enforces strict risk management (10% position sizing) and hard stop-losses.
    """
    try:
        from obsidian_trading_mastermind import trading_mastermind
        return await trading_mastermind.execute_obsidian_trade_strike()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def get_obsidian_ledger() -> list:
    """
    Returns the real-time balance ledger for all grid accounts.
    Tracks Obsidian Ingress (Standard), ObsidianBridge, Square, and Robinhood.
    """
    try:
        from obsidian_account_ledger import account_ledger
        return account_ledger.get_all_entries()
    except Exception as e:
        return [{"error": str(e)}]

@mcp.tool()
async def trigger_system_self_heal() -> dict:
    """
    Triggers the Obsidian Daemon Core to perform a full system watchdog audit.
    Restarts crashed processes and verifies 100/100 reputation score.
    """
    try:
        from obsidian_daemon_core import daemon_core
        await daemon_core.run_self_heal_cycle()
        return {"status": "SUCCESS", "message": "System-wide self-heal initiated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def trigger_capital_sweep(destination: str = "BITCOIN_CASH_APP") -> str:
    from obsidian_capital_hub_controller import capital_hub
    await capital_hub.trigger_emergency_payout_sweep(destination)
    return f"Obsidian Sweep to [{destination}] ($obsidianco) successfully initiated."

@mcp.tool()
async def get_definite_chief_aim() -> dict:
    """
    Returns the Definite Chief Aim based on Napoleon Hill's 'Think and Grow Rich'.
    Used for focus and alignment of the Master Mind alliance.
    """
    from obsidian_definite_chief_aim import get_definite_chief_aim
    return get_definite_chief_aim()

@mcp.tool()
async def dispatch_god_mission(goal: str) -> dict:
    from obsidian_god_mission_control import god_mission_control
    res = await god_mission_control.architect_and_dispatch_mission(goal)
    return res.model_dump()

@mcp.tool()
async def trigger_mass_linking_strike(limit: int = 50) -> dict:
    """
    Executes a mass-linking strike to connect Obsidian Ingress accounts to the ObsidianBridge ID.
    This ensures all ghost accounts funnel their yield to the Director's BTC Hub.
    """
    try:
        from obsidian_hg_linker import linker
        count = await linker.execute_mass_linking_strike(limit)
        return {"status": "SUCCESS", "accounts_linked": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def trigger_wholesale_market_strike() -> dict:
    """
    Finds and pitches the 5,000-IP mesh to high-ticket wholesale buyers (AI labs).
    Goal: Secure a $5,000/month recurring daily retainer.
    """
    try:
        from obsidian_market_scout import market_scout
        count = await market_scout.scout_and_strike_wholesale()
        return {"status": "SUCCESS", "proposals_sent": count}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def trigger_penta_stack_pulse() -> dict:
    """
    Multiplies grid yield by 5x by running 5 mining apps on every residential port.
    """
    try:
        from obsidian_penta_stacker import penta_stacker
        await penta_stacker.execute_stacking_strike()
        return {"status": "SUCCESS", "message": "Penta-Stack Loaded on 100 ports."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def trigger_private_grid_pulse() -> dict:
    """
    Executes a high-frequency internal grid pulse.
    Synchronizes 5,000+ private sentinel nodes and triggers the BTC sweep.
    No leasing. No third parties. 100% Personal Access.
    """
    try:
        from obsidian_aggregator_core import aggregator_core
        from obsidian_obsidian_bridge_autoclaim import jmpt_autoclaim
        # 1. Sync Private Swarm
        await aggregator_core.synchronize_private_swarm()
        # 2. Sweep to Bitcoin
        await jmpt_autoclaim.execute_obsidian_extraction_blitz()
        return aggregator_core.get_private_wealth_audit()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def trigger_global_termination() -> dict:
    """
    Kills all active swarm processes and collapses the grid.
    Reserved for Obsidian Christopher (God Special Access).
    """
    try:
        from obsidian_kill_switch import kill_switch
        await kill_switch.execute_global_termination()
        return {"status": "SUCCESS", "message": "Grid Terminated. Systems Offline."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def execute_ghost_protocol() -> dict:
    """
    Purges all digital traces, logs, and identities.
    Reserved for Obsidian Christopher (God Special Access).
    """
    try:
        from obsidian_ghost_protocol import ghost_protocol
        ghost_protocol.execute_ghost_purge()
        return {"status": "SUCCESS", "message": "Digital traces incinerated."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def trigger_capital_flip() -> dict:
    from obsidian_capital_flip_engine import flip_engine
    return await flip_engine.monitor_and_flip_gains()

@mcp.tool()
async def allocate_revenue_to_treasury(amount_usd: float, source: str = "GENERAL") -> dict:
    from obsidian_treasury_manager import treasury_manager
    return await treasury_manager.allocate_incoming_revenue(amount_usd, source)

@mcp.tool()
async def get_robinhood_portfolio_summary() -> dict:
    """
    Fetches Robinhood portfolio balances, buying power, and active crypto holdings.
    """
    try:
        from robinhood_mcp_bridge import robinhood_bridge
        return await robinhood_bridge.get_portfolio_summary()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def execute_robinhood_trade(symbol: str = "BTC", action: str = "BUY", amount_usd: float = 100.0) -> dict:
    """
    Executes an automated limit order on Robinhood with strict -1.5% stop-loss protection.
    """
    try:
        from robinhood_mcp_bridge import robinhood_bridge
        return await robinhood_bridge.execute_algorithmic_trade(symbol, action, amount_usd)
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def rotate_quantum_keys() -> dict:
    """
    Generates a fresh set of Post-Quantum Cryptography (PQC) session keys.
    Neutralizes the threat of high-level decryption and secures the grid.
    """
    try:
        from obsidian_quantum_keys import quantum_keys
        return quantum_keys.generate_pqc_session_key("Obsidian_Grid_Rotation")
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def audit_corporate_umbrella() -> dict:
    """
    Performs a legal and financial 'Umbrella' audit to ensure maximum asset protection.
    Identifies 'Loop Holes' for tax and risk optimization.
    """
    try:
        from obsidian_corporate_shield import corporate_shield
        return corporate_shield.get_umbrella_structure()
    except Exception as e:
        return {"status": "error", "message": str(e)}

@mcp.tool()
async def trigger_high_greed_strike(channel: str = "PINTEREST") -> dict:
    from obsidian_revenue_multiplier import revenue_multiplier
    return await revenue_multiplier.generate_high_greed_marketing_strike(channel)

@mcp.tool()
async def provision_geospatial_layer(layer_name: str) -> dict:
    from obsidian_geospatial_sdi import geospatial_sdi
    return await geospatial_sdi.create_interactive_map_layer(layer_name)

@mcp.tool()
async def draft_direct_b2b_contract(company_name: str, service: str = "PRIVATE_PROXY_PORT") -> dict:
    from obsidian_direct_sales_hub import direct_sales_hub
    return await direct_sales_hub.create_direct_b2b_contract(company_name, service)

@mcp.tool()
async def close_revenue_loop() -> dict:
    from square_real_balance_monitor import square_balance_monitor
    from depin_aggregator_supervisor import depin_supervisor
    sq_res = await square_balance_monitor.get_actual_bank_balance()
    sup_res = await depin_supervisor.run_247_health_supervisor_check()
    return {
        "status": "OBSIDIAN_READY",
        "square_balance_usd": sq_res.get("actual_proposal sent_funds", 0.0),
        "network_health": f"{sup_res.get('network_uptime_percentage')}%",
        "message": "Loop Closed. Empire is synchronized."
    }

if __name__ == "__main__":
    mcp.run()
