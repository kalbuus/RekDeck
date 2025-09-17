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

def is_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except OSError:
        return False


def connect_wifi(ssid, password=None):
    try:
        if password:
            result = subprocess.run(
                ["nmcli", "dev", "wifi", "connect", ssid, "password", password],
                capture_output=True, text=True, check=True
            )
        else:
            result = subprocess.run(
                ["nmcli", "dev", "wifi", "connect", ssid],
                capture_output=True, text=True, check=True
            )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return False, e.stderr.strip()
