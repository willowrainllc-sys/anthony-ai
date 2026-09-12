# --- EMPIRE MULTI-INTERFACE NETWORK ROUTER & BANDWIDTH AGGREGATOR v1.0 ---
import os
import sys
import json
import socket
import psutil
import asyncio
import httpx
from pathlib import Path
from swarm_logger import swarm_log
from swarm_persistence import db

class MultiInterfaceNetworkRouter:
    """
    MULTI-INTERFACE NETWORK ROUTER:
    Detects all active network adapters (Wi-Fi, Ethernet, Cellular, Secondary NICs)
    and enables multi-homed socket binding so background nodes (Mysterium, Obsidian Ingress,
    EarnApp, Pawns) can route outbound traffic independently through specific local network adapters.
    """
    def __init__(self):
        self.active_interfaces = []
        self.refresh_interfaces()

    def refresh_interfaces(self) -> list:
        """Scans system network interfaces and collects active IPv4 addresses."""
        self.active_interfaces = []
        try:
            addrs = psutil.net_if_addrs()
            stats = psutil.net_if_stats()

            for iface_name, iface_addresses in addrs.items():
                iface_stat = stats.get(iface_name)
                # Only include active, up interfaces that are not loopback
                if iface_stat and iface_stat.isup:
                    for addr in iface_addresses:
                        if addr.family == socket.AF_INET and not addr.address.startswith("127."):
                            self.active_interfaces.append({
                                "interface_name": iface_name,
                                "ip_address": addr.address,
                                "netmask": addr.netmask,
                                "speed_mbps": iface_stat.speed
                            })
        except Exception as e:
            swarm_log(f"[-] Interface Scan Note: {e}", node="ROUTER")

        swarm_log(f" ROUTER: Detected {len(self.active_interfaces)} active local network interface(s).", node="ROUTER")
        return self.active_interfaces

    def get_httpx_client_for_interface(self, local_ip: str, timeout: float = 15.0) -> httpx.AsyncClient:
        """
        Creates an httpx.AsyncClient bound to a specific local IP address / interface.
        Enables multi-homed outbound traffic routing per node.
        """
        transport = httpx.AsyncHTTPTransport(local_address=local_ip)
        return httpx.AsyncClient(transport=transport, timeout=timeout)

    async def probe_interface_outbound_speed(self, local_ip: str) -> dict:
        """Tests outbound connectivity and IP routing through a specific network interface."""
        try:
            async with self.get_httpx_client_for_interface(local_ip, timeout=10.0) as client:
                res = await client.get("https://api.ipify.org?format=json")
                if res.status_code == 200:
                    public_ip = res.json().get("ip")
                    return {
                        "local_ip": local_ip,
                        "public_ip": public_ip,
                        "status": "ONLINE_BOUND"
                    }
        except Exception as e:
            swarm_log(f"[-] Interface Probe Note for {local_ip}: {e}", node="ROUTER")

        return {
            "local_ip": local_ip,
            "public_ip": "DEFAULT_GATEWAY",
            "status": "ACTIVE_DEFAULT"
        }

    async def get_multi_interface_summary(self) -> dict:
        """Generates a complete multi-interface routing summary for all background nodes."""
        self.refresh_interfaces()
        probes = []

        for iface in self.active_interfaces:
            ip = iface["ip_address"]
            probe_res = await self.probe_interface_outbound_speed(ip)
            probes.append({
                "interface": iface["interface_name"],
                "local_ip": ip,
                "public_exit_ip": probe_res["public_ip"],
                "speed_mbps": iface["speed_mbps"],
                "status": probe_res["status"]
            })

        summary = {
            "status": "success",
            "total_interfaces": len(probes),
            "multi_homed_routing": "ENABLED",
            "interfaces": probes
        }

        db.log_event("ROUTER", "MULTI_INTERFACE_ROUTING_ACTIVE", summary)
        return summary

multi_interface_router = MultiInterfaceNetworkRouter()

if __name__ == "__main__":
    res = asyncio.run(multi_interface_router.get_multi_interface_summary())
    print("MULTI-INTERFACE NETWORK ROUTER SUMMARY:")
    print(json.dumps(res, indent=2))
