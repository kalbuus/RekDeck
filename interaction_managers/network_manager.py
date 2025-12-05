import json
from kivy.app import App

class WebSocketClient:
    def __init__(self, uri):
        self.uri = uri
        self.connection = None

    async def connect(self):
        from websockets import connect
        self.connection = await connect(self.uri)
        return self.connection

    async def send(self, message: dict):
        if self.connection is None:
            await self.connect()
        message = json.dumps(message)
        await self.connection.send(message)

    async def receive(self):
        if self.connection is None:
            await self.connect()
        try:
            response = await self.connection.recv()
            try:
                return json.loads(response)
            except Exception:
                return response
        except Exception as e:
            # Проверяем, закрыто ли соединение сервером
            if hasattr(self.connection, 'close_code') and self.connection.close_code is not None:

                App.get_running_app().on_disconnect()
            else:
                print(f"[WebSocket] Ошибка при получении: {e}")
            raise

    async def close(self):
        if self.connection:
            await self.connection.close()
            self.connection = None
import subprocess
import socket
import ipaddress
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from websockets import connect
import asyncio

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
        subprocess.run(
            ["nmcli", "connection", "delete", ssid],
            capture_output=True, text=True
        )
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
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return None

async def _check_host(ip, port):
    """Попытка подключиться к серверу на ip:PORT."""
    try:
        uri = f"ws://{ip}:{port}"
        async with connect(uri):
            return ip
    except Exception:
        return None

async def find_server_on_lan(port=8765):
    is_debug = os.name == 'nt'
    if is_debug:
        return '127.0.0.1'

    local_ip = _get_local_ip()
    subnet = ".".join(local_ip.split(".")[:-1])

    tasks = []
    for i in range(1, 255):
        ip = f"{subnet}.{i}"
        tasks.append(_check_host(ip, port))

    results = await asyncio.gather(*tasks)
    servers = [ip for ip in results if ip]
    return servers[0] if len(servers) > 0 else None