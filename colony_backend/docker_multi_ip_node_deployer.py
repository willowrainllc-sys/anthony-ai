# --- EMPIRE DOCKER MULTI-IP BANDWIDTH NODE DEPLOYER v1.0 ---
import os
import sys
import json
import uuid
from pathlib import Path
from colony_logger import colony_log
from colony_persistence import db

SECURE_DIR = Path(r"D:\ObsidianAi_Colony\Secure_Assets")
DOCKER_VAULT = SECURE_DIR / "docker_multi_ip_configs"
DOCKER_VAULT.mkdir(parents=True, exist_ok=True)

class DockerMultiIpNodeDeployer:
    """
    DOCKER MULTI-IP NODE DEPLOYER v1.0:
    Generates Docker Compose & macvlan IP alias binding configurations
    to run multiple Obsidian Ingress, EarnApp, Pawns, and Mysterium nodes
    on distinct IP addresses on a single server machine.
    """
    def generate_multi_ip_docker_compose(self, ip_addresses: list = None) -> dict:
        if not ip_addresses:
            ip_addresses = ["192.168.1.101", "192.168.1.102", "192.168.1.103", "192.168.1.104"]

        colony_log(f"DOCKER_IP: Generating multi-IP Docker configuration across {len(ip_addresses)} distinct IPs...", node="DOCKER_IP")

        docker_services = {}
        for idx, ip_addr in enumerate(ip_addresses, 1):
            docker_services[f"obsidian_ingress_node_{idx}"] = {
                "image": "obsidian_ingress/obsidian_ingress:latest",
                "container_name": f"hg_node_{idx}",
                "restart": "always",
                "networks": {
                    "macvlan_net": {
                        "ipv4_address": ip_addr
                    }
                },
                "environment": [
                    "OBSIDIAN_INGRESS_SDK_KEY=TCCM2JLD5UU32WF3XG9MHZV1",
                    "ACCOUNT_EMAIL=obsidian.global.holdings@gmail.com"
                ]
            }

            docker_services[f"earnapp_node_{idx}"] = {
                "image": "fazalfarhan01/earnapp:latest",
                "container_name": f"ea_node_{idx}",
                "restart": "always",
                "networks": {
                    "macvlan_net": {
                        "ipv4_address": ip_addr
                    }
                },
                "environment": [
                    "EARNAPP_AUTH_KEY=PERSONA_VAULT_GMAIL_OAUTH"
                ]
            }

        compose_config = {
            "version": "3.8",
            "networks": {
                "macvlan_net": {
                    "driver": "macvlan",
                    "driver_opts": {
                        "parent": "eth0"
                    },
                    "ipam": {
                        "config": [
                            {
                                "subnet": "192.168.1.0/24",
                                "gateway": "192.168.1.1"
                            }
                        ]
                    }
                }
            },
            "services": docker_services
        }

        # Save docker-compose.yml
        out_file = DOCKER_VAULT / "docker-compose-multi-ip.yml"
        with open(out_file, "w") as f:
            json.dump(compose_config, f, indent=4)

        db.log_event("DOCKER_IP", "MULTI_IP_COMPOSE_GENERATED", {
            "ip_count": len(ip_addresses),
            "ip_list": ip_addresses,
            "vault_path": str(out_file)
        })

        colony_log(f" DOCKER_IP SUCCESS: Multi-IP Docker config generated at {out_file.name}!", node="DOCKER_IP")
        return {
            "status": "success",
            "ip_count": len(ip_addresses),
            "docker_compose_file": str(out_file),
            "instructions": "Run 'docker-compose -f docker-compose-multi-ip.yml up -d' on your server to launch all nodes on distinct IPs!"
        }

docker_ip_deployer = DockerMultiIpNodeDeployer()

if __name__ == "__main__":
    res = docker_ip_deployer.generate_multi_ip_docker_compose()
    print("DOCKER MULTI-IP CONFIGURATION DEPLOYMENT:")
    print(json.dumps(res, indent=2))
