import base64
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
import os

def generate_keys():
    print("[*] [FINANCIAL HUB] Generating ed25519 Key Pair for Robinhood API...")

    # 1. Generate Private Key
    private_key = ed25519.Ed25519PrivateKey.generate()

    # 2. Get Public Key
    public_key = private_key.public_key()

    # 3. Encode Public Key to Base64 (Required by Robinhood)
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )
    public_base64 = base64.b64encode(public_bytes).decode('utf-8')

    # 4. Save Private Key Securely
    # We save it in a PEM format for the machine to use later
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.NoEncryption()
    )

    save_path = r"C:\Users\willo\OneDrive\Desktop\Anthony_Ai\swarm_vault\robinhood_private.pem"
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as f:
        f.write(private_bytes)

    print("-" * 50)
    print(f"[[*]] SUCCESS: Private Key saved to: {save_path}")
    print("\n[IMPORTANT] Copy the Public Key below and paste it into the Robinhood 'API Trading' section:")
    print("-" * 50)
    print(f"\n{public_base64}\n")
    print("-" * 50)

if __name__ == "__main__":
    generate_keys()
