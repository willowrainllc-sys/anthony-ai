import asyncio
import json
import os
import sys

# Ensure imports from current directory work
sys.path.append(os.path.dirname(__file__))

from obsidian_aggregator_core import aggregator_core
from master_studio import master_factory
from obsidian_quantum_keys import quantum_keys
from square_real_balance_monitor import square_balance_monitor
from depin_aggregator_supervisor import depin_supervisor

async def main():
    print("--- Initiating Obsidian God-Mode Burst ---")

    # 1. Trigger 5k Aggregator Burst
    print("\n[1/4] Triggering 5k Aggregator Burst for SpaceX_Data_Logistics...")
    await aggregator_core.synchronize_virtual_colony()
    burst_res = await aggregator_core.generate_b2b_wholesale_invoice(
        client_name='SpaceX_Data_Logistics',
        volume_gb=865.0
    )
    print(f"Result: {json.dumps(burst_res, indent=2)}")

    # 2. Trigger Master Burst
    print("\n[2/4] Launching 9-minute professional documentary (future_cyber_tech)...")
    master_res = await master_factory.produce_and_dispatch_episode(
        channel_id="ANTHONY_AI_OFFICIAL",
        category='future_cyber_tech',
        ep_num=1,
        target_min=9,
        content_type="LONG_FORM"
    )
    print(f"Result: {json.dumps(master_res, indent=2)}")

    # 3. Rotate Quantum Keys
    print("\n[3/4] Rotating Quantum Keys...")
    quantum_res = quantum_keys.generate_pqc_session_key("Obsidian_Grid_Rotation")
    print(f"Result: {json.dumps(quantum_res, indent=2)}")

    # 4. Verify Grid Status
    print("\n[4/4] Verifying Grid Status...")
    sq_res = await square_balance_monitor.get_actual_bank_balance()
    sup_res = await depin_supervisor.run_247_health_supervisor_check()

    status_summary = {
        "status": "OBSIDIAN_READY",
        "revenue_locked_usd": sq_res.get("actual_proposal sent_funds", 0.0),
        "security_status": quantum_res.get("status"),
        "network_health": f"{sup_res.get('network_uptime_percentage')}%",
        "quantum_key_id": quantum_res.get("key_id"),
        "message": "Obsidian God-Mode Burst Complete. Empire is synchronized."
    }

    print("\n--- FINAL STATUS SUMMARY ---")
    print(json.dumps(status_summary, indent=2))

if __name__ == "__main__":
    asyncio.run(main())
