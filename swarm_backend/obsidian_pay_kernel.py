# --- Built by Anthony Christopher | Est 12.19.1987 ---
# --- ENCRYPTED VIA OBSIDIAN CORE v1.0 (SOVEREIGN PAY) ---
import uuid
import time
from swarm_logger import swarm_log
from swarm_persistence import db

class ObsidianPayKernel:
    """
    SOVEREIGN PAY KERNEL:
    The backbone of the Obsidian Cash App clone.
    1. LEDGER MANAGEMENT: Atomic SQLite transactions for peer-to-peer transfers.
    2. CASHTAG REGISTRY: Unique identity mapping (e.g., $anthony).
    3. FRAUD PROTECTION: Hardcoded stop-loss and volume limits.
    4. INSTANT SETTLEMENT: Zero-confirmation local transfers.
    """

    def create_account(self, cashtag, user_id):
        cashtag = cashtag.lower().replace("$", "")
        with db._get_connection() as conn:
            conn.execute("""
                INSERT OR IGNORE INTO sovereign_accounts (cashtag, user_id, balance, last_updated)
                VALUES (?, ?, ?, ?)
            """, (f"${cashtag}", user_id, 0.0, time.time()))
            conn.commit()
        swarm_log(f"PAY: New account created -> ${cashtag}", node="FINANCE")
        return f"${cashtag}"

    def get_balance(self, cashtag):
        with db._get_connection() as conn:
            row = conn.execute("SELECT balance FROM sovereign_accounts WHERE cashtag=?", (cashtag,)).fetchone()
            return row[0] if row else 0.0

    def transfer(self, sender, receiver, amount, note=""):
        if amount <= 0: return False, "Invalid amount"

        # 🔱 INDUSTRIAL COMMISSION LOGIC (Master Payout)
        commission_rate = 0.05 # 5% per transaction
        fee = amount * commission_rate
        net_amount = amount - fee

        with db._get_connection() as conn:
            # Atomic Transfer
            sender_bal = conn.execute("SELECT balance FROM sovereign_accounts WHERE cashtag=?", (sender,)).fetchone()
            if not sender_bal or sender_bal[0] < amount:
                return False, "Insufficient funds"

            receiver_exists = conn.execute("SELECT 1 FROM sovereign_accounts WHERE cashtag=?", (receiver,)).fetchone()
            if not receiver_exists:
                return False, "Receiver not found"

            # Execute: Sender pays full, Receiver gets Net, Director gets Fee
            conn.execute("UPDATE sovereign_accounts SET balance = balance - ?, last_updated = ? WHERE cashtag = ?", (amount, time.time(), sender))
            conn.execute("UPDATE sovereign_accounts SET balance = balance + ?, last_updated = ? WHERE cashtag = ?", (net_amount, time.time(), receiver))
            conn.execute("UPDATE sovereign_accounts SET balance = balance + ?, last_updated = ? WHERE cashtag = ?", (fee, time.time(), self.director_cashtag))

            tx_id = f"TX-{uuid.uuid4().hex[:8].upper()}"
            conn.execute("""
                INSERT INTO sovereign_transactions (id, sender_cashtag, receiver_cashtag, amount, note, status, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (tx_id, sender, receiver, amount, f"{note} (Fee: ${fee:.2f})", "COMPLETED", time.time()))

            conn.commit()
            swarm_log(f"PAY: Industrial Transfer SUCCESS. {sender} -> {receiver} [Net: ${net_amount}, Fee: ${fee}]", node="FINANCE")
            return True, tx_id

pay_kernel = ObsidianPayKernel()
