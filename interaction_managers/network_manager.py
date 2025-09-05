import subprocess
import socket
import ipaddress

def scan_wifi(is_debug: bool):
    if is_debug: 
        return [
            {'ssid': 'TestNetwork1', 'requires_password': True}, 
            {'ssid': 'TestNetwork2', 'requires_password': True},
            {'ssid': 'TestNetwork3', 'requires_password': False}]
    
    result = subprocess.run(
        ["nmcli", "-t", "-f", "SSID,SECURITY", "dev", "wifi", "list"],
        capture_output=True, text=True
    )

    networks = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        ssid, security = line.split(":", 1)
        requires_password = bool(security.strip())
        networks.append({
            "ssid": ssid,
            "requires_password": requires_password
        })

    return networks