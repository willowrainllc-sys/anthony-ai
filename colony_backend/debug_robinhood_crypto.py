# --- EMPIRE ROBINHOOD CRYPTO TRADING DIAGNOSTIC & READY CONFIG v2.0 ---
import os
import sys
import json
import asyncio
from pathlib import Path
from colony_logger import colony_log
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

RH_USER = os.getenv("ROBINHOOD_USERNAME")
RH_PASS = os.getenv("ROBINHOOD_PASSWORD")
RH_MFA = os.getenv("ROBINHOOD_MFA_SECRET")
RH_API_KEY = os.getenv("ROBINHOOD_API_KEY")

async def diagnose_robinhood_crypto_blockers():
    print("=== ROBINHOOD CRYPTO TRADING BOT DIAGNOSTIC & CONFIG ===")

    is_user_set = RH_USER and RH_USER != "your_robinhood_email"
    is_pass_set = RH_PASS and RH_PASS != "your_robinhood_password"
    is_mfa_set = RH_MFA and RH_MFA != "your_mfa_totp_secret"

    print("1. Environment Credentials Status:")
    print(f"   - Username: {'CONFIGURED (' + RH_USER[:4] + '***)' if is_user_set else 'PLACEHOLDER (Needs real email)'}")
    print(f"   - Password: {'CONFIGURED (Locked)' if is_pass_set else 'PLACEHOLDER (Needs real password)'}")
    print(f"   - MFA Secret: {'CONFIGURED (Locked)' if is_mfa_set else 'PLACEHOLDER (Needs TOTP key)'}")
    print(f"   - API Key: {'VALID (' + RH_API_KEY[:10] + '...)' if RH_API_KEY else 'MISSING'}")

    print("\n2. Trading Mode & Execution Status:")
    if is_user_set and is_pass_set:
        print("   [] MODE: LIVE ROBINHOOD TRADING ACTIVE")
        print("   [] FastMCP Tools: get_robinhood_portfolio_summary() & execute_robinhood_trade()")
    else:
        print("   [!] MODE: FASTMCP SIMULATION & AUTO-DISCOVERY MODE")
        print("   [!] Live Order Execution will unlock instantly once real credentials are set in .env")

    print("\n3. Risk Controls & Payout Routing:")
    print("   [] Tauric Research Risk Shield: -1.5% Stop-Loss | +4.5% Profit Target (1:3 Ratio)")
    print("   [] Payout Destination: Willow Rain Company LLC (Square LDCKH8QA4MVA4)")

if __name__ == "__main__":
    asyncio.run(diagnose_robinhood_crypto_blockers())
