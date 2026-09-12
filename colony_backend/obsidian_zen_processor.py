# --- Built by Anthony Christopher | Est 12.19.1987 ---
import sqlite3
import json
import time
import os

def process_registration(data):
    """
    Acts as an API endpoint logic to receive form data from the onboarding page.
    """
    legal_name = data.get('legal_name', 'Unknown')
    business_type = data.get('type', 'LLC')
    state = data.get('state', 'CO')
    email = data.get('email', 'N/A')

    status = "PROPOSAL_SENT"
    print(f"[*] Received new business proposal: {legal_name} ({business_type}) in {state}")

    # 1. Update Empire_Vault.db
    db_path = "Empire_Vault.db"
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS zen_registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                legal_name TEXT,
                business_type TEXT,
                state TEXT,
                email TEXT,
                status TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            INSERT INTO zen_registrations (legal_name, business_type, state, email, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (legal_name, business_type, state, email, status))

        conn.commit()
        conn.close()
        print(f"[+] Empire_Vault.db updated for Titan: {legal_name}")
    except Exception as e:
        print(f"[!] Error updating Empire_Vault.db: {e}")

    # 2. Simulate 'Mailing' a physical certificate using DocuPost API placeholder
    simulate_docupost_mail(legal_name, state)

    return {"status": "NEGOTIATING", "message": "Proposal processed and vault updated."}

def simulate_docupost_mail(name, state):
    """
    Placeholder for DocuPost API integration.
    """
    print(f"[*] Initiating Physical Certificate Dispatch for {name}...")
    # DOCUPOST_API_KEY = "sk_live_xxxxxxxxxxxx"
    # payload = { "to": name, "address": "...", "content": f"Official Certificate for {name} in {state}" }
    time.sleep(1) # Simulating API latency
    print(f"[+] DocuPost Placeholder: Mail dispatched to {state} Department of Revenue.")

if __name__ == "__main__":
    # Mock data for testing
    test_data = {
        "legal_name": "Obsidian Global Holdings",
        "type": "LLC",
        "state": "MO",
        "email": "ceo@obsidian.com"
    }
    result = process_registration(test_data)
    print(f"Final Outcome: {result}")
