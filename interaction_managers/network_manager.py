import subprocess
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

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


def _get_local_ip():
    """Попытаться определить локальный IP машины (без внешнего запроса)."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # не посылаем данные, просто подключаемся к публичному адресному UDP чтобы узнать интерфейс
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        # fallback
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return None


def find_server_on_lan(port=6789, timeout=0.3, is_debug=False, max_workers=60):
    """
    Ищет хост с открытым TCP-портом `port` в локальной /24 подсети устройства.
    Возвращает IP найденного хоста или None.
    """
    if is_debug or os.name == 'nt': # В режиме отладки возвращаем localhost
        return '127.0.0.1'

    local_ip = _get_local_ip()
    if not local_ip:
        return None

    parts = local_ip.split('.')
    if len(parts) != 4:
        return None
    base = '.'.join(parts[:3]) + '.'
    own_last = parts[3]

    ips = [base + str(i) for i in range(1, 255) if str(i) != own_last]

    def _check(ip):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(timeout)
                s.connect((ip, port))
            return ip
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        futures = {exe.submit(_check, ip): ip for ip in ips}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                return res
    return None
