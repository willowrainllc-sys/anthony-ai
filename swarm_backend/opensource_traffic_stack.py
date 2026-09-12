# --- EMPIRE OPEN-SOURCE TRAFFIC STACK & MESH ROUTING ORCHESTRATOR v1.2 ---
import os
import sys
import json
import uuid
import time
import random
import asyncio
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from pathlib import Path

from swarm_logger import swarm_log
from swarm_persistence import db
from square_checkout_gateway import square_gateway
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

SECURE_DIR = Path(r"D:\ObsidianAi_Swarm\Secure_Assets")
TRAFFIC_VAULT = SECURE_DIR / "opensource_traffic_vault"
TRAFFIC_VAULT.mkdir(parents=True, exist_ok=True)

# ============================================================
# PHASE 1 & 2 SCHEMAS: TRAFFIC STACK & METERED PROVISIONING
# ============================================================

class ProxyCredential(BaseModel):
    client_id: str
    username: str
    password: str
    host_ip: str = "47.85.50.46"
    http_port: int = 8000
    socks5_port: int = 1080
    bandwidth_quota_gb: float = 100.0
    created_at: float = Field(default_factory=time.time)
    is_active: bool = True

class TrafficMeshNode(BaseModel):
    node_id: str
    node_name: str
    provider: str            # "Oracle_Free_ARM", "AWS_Free_Tier", "Local_Edge"
    wireguard_mesh_ip: str
    public_ip: str
    assigned_ports: List[int]
    status: str = "ONLINE"

class OpenSourceTrafficStack:
    """
    OPEN-SOURCE TRAFFIC STACK & MESH ORCHESTRATOR v1.2:
    Phase 1: Envoy/3proxy Gateway & WireGuard NetBird Private Mesh Layer.
    Phase 2: FastAPI / Supabase Usage Metering & Auto-Provisioning.
    Phase 3: Hybrid Cloud (Oracle Free Tier / AWS / Edge Tunnels).
    """
    def __init__(self):
        self.nodes = [
            TrafficMeshNode(node_id="node_midwest", node_name="Midwest Edge Node", provider="Local_Edge", wireguard_mesh_ip="10.0.0.1", public_ip="47.85.50.46", assigned_ports=[8000, 1080]),
            TrafficMeshNode(node_id="node_oracle_01", node_name="Oracle Free Cloud 01", provider="Oracle_Free_ARM", wireguard_mesh_ip="10.0.0.2", public_ip="129.146.10.15", assigned_ports=[8001, 1081]),
            TrafficMeshNode(node_id="node_oracle_02", node_name="Oracle Free Cloud 02", provider="Oracle_Free_ARM", wireguard_mesh_ip="10.0.0.3", public_ip="129.146.10.16", assigned_ports=[8002, 1082]),
            TrafficMeshNode(node_id="node_aws_01", node_name="AWS Free Tier Micro", provider="AWS_Free_Tier", wireguard_mesh_ip="10.0.0.4", public_ip="54.210.88.42", assigned_ports=[8003, 1083])
        ]

    def generate_3proxy_config(self) -> str:
        """Phase 1: Generates open-source 3proxy configuration file for SOCKS5/HTTP translation."""
        config_lines = [
            "# --- OPEN-SOURCE 3PROXY CONFIGURATION ---",
            "daemon",
            "nserver 8.8.8.8",
            "nserver 1.1.1.1",
            "log /var/log/3proxy.log D",
            "auth strong",
            ""
        ]

        for node in self.nodes:
            config_lines.append(f"# Node: {node.node_name} ({node.provider})")
            config_lines.append(f"proxy -p{node.assigned_ports[0]} -i{node.wireguard_mesh_ip} -e{node.public_ip}")
            config_lines.append(f"socks -p{node.assigned_ports[1]} -i{node.wireguard_mesh_ip} -e{node.public_ip}")
            config_lines.append("")

        cfg_text = "\n".join(config_lines)
        cfg_path = TRAFFIC_VAULT / "3proxy.cfg"
        with open(cfg_path, "w") as f:
            f.write(cfg_text)

        swarm_log(f" TRAFFIC_STACK: Generated 3proxy config at {cfg_path.name}!", node="TRAFFIC_STACK")
        return cfg_text

    async def provision_client_proxy_access(self, client_email: str, quota_gb: float = 100.0) -> dict:
        """Phase 2: Programmatically provisions credentials upon Square payment webhook."""
        client_id = f"client_{uuid.uuid4().hex[:6]}"
        username = f"user_{client_email.split('@')[0]}"
        password = f"secret_{uuid.uuid4().hex[:8]}"

        node = random.choice(self.nodes)

        cred = ProxyCredential(
            client_id=client_id,
            username=username,
            password=password,
            host_ip=node.public_ip,
            http_port=node.assigned_ports[0],
            socks5_port=node.assigned_ports[1],
            bandwidth_quota_gb=quota_gb
        )

        # Generate Square 1-Click Payment Link ($49/mo)
        sq_res = await square_gateway.create_digital_product_checkout(f"Willow Rain Network Pipe ({quota_gb} GB)", price_usd=49.00)

        # --- SUPABASE PROVISIONING SYNC ---
        try:
            from supabase import create_client
            s_url = os.getenv("SUPABASE_URL")
            s_key = os.getenv("SUPABASE_KEY")
            if s_url and s_key:
                supabase = create_client(s_url, s_key)
                supabase.table("proxy_clients").insert({
                    "client_id": client_id,
                    "email": client_email,
                    "username": username,
                    "password": password,
                    "host_ip": node.public_ip,
                    "quota_gb": quota_gb,
                    "is_active": True
                }).execute()
                swarm_log(f" TRAFFIC_STACK: Client {client_id} synced to Supabase Cloud.", node="TRAFFIC_STACK")
        except Exception as e:
            swarm_log(f"[-] Supabase Proxy Sync Note: {e}", node="TRAFFIC_STACK")

        swarm_log(f" TRAFFIC_STACK SUCCESS: Provisioned {quota_gb} GB proxy access for {client_email}!", node="TRAFFIC_STACK")

        return {
            "status": "PROVISIONED",
            "client_id": client_id,
            "username": username,
            "password": password,
            "connection_strings": {
                "http_proxy": f"http://{username}:{password}@{node.public_ip}:{node.assigned_ports[0]}",
                "socks5_proxy": f"socks5://{username}:{password}@{node.public_ip}:{node.assigned_ports[1]}"
            },
            "allocated_node": node.node_name,
            "square_checkout_url": sq_res.get("checkout_url")
        }

opensource_traffic_stack = OpenSourceTrafficStack()

if __name__ == "__main__":
    cfg = opensource_traffic_stack.generate_3proxy_config()
    print("3PROXY OPEN-SOURCE CONFIGURATION:")
    print(cfg)

    async def test_provision():
        res = await opensource_traffic_stack.provision_client_proxy_access("enterprise_client@example.com", 250.0)
        print("\nPROVISIONED CLIENT PROXY ACCESS:")
        print("Username:", res["username"])
        print("SOCKS5 Proxy:", res["connection_strings"]["socks5_proxy"])
        print("Square Checkout Link:", res["square_checkout_url"])

    asyncio.run(test_provision())
