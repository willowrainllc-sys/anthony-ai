import asyncio
import os
import sys
from robinhood_node import RobinhoodNode, safe_print
from commerce_core import CommerceCore
from dotenv import load_dotenv

# Load env from root
from pathlib import Path
load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

async def test_all():
    safe_print("--- STARTING NODE TEST SEQUENCE ---")

    # 1. Test Robinhood Trade
    safe_print("Testing Robinhood AI Trade Strike...")
    rh = RobinhoodNode()
    # Mocking a high-velocity trend
    rh_res = await rh.hit_the_market("Bitcoin is skyrocketing due to leaked institutional plans")
    safe_print(f"Robinhood Result: {rh_res}")

    # 2. Test Printful Sync
    safe_print("Testing Printful Multi-Store Sync...")
    commerce = CommerceCore()
    # Mocking a design ID (assumes existence in bucket or just testing the API call)
    comm_res = await commerce.create_pod_bridge("test_design_123", "Test Trend Aurora")
    safe_print(f"Commerce Result: {comm_res}")

    safe_print("--- TEST SEQUENCE COMPLETE ---")

if __name__ == "__main__":
    asyncio.run(test_all())
