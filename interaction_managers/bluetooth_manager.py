import json
import os

BT_UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


def start_bt_agent() -> tuple:
    """Start a bluetoothctl agent that auto-confirms pairing requests.
    Returns (proc, status_message)."""
    import subprocess
    import threading
    addr = _get_local_bt_address()
    try:
        proc = subprocess.Popen(
            ["bluetoothctl"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        proc.stdin.write(b"agent on\ndefault-agent\npairable on\ndiscoverable on\n")
        proc.stdin.flush()

        def _auto_confirm():
            while True:
                try:
                    line = proc.stdout.readline()
                    if not line:
                        break
                    text = line.decode("utf-8", errors="ignore").strip()
                    print(f"[BT agent] {text}")
                    if any(kw in text.lower() for kw in ["confirm", "authorize", "yes/no"]):
                        proc.stdin.write(b"yes\n")
                        proc.stdin.flush()
                except Exception:
                    break

        threading.Thread(target=_auto_confirm, daemon=True).start()
        return proc, f"Pi is visible & pairable\nAddr: {addr}\nPair from Windows Bluetooth settings"
    except Exception as e:
        return None, f"Could not start BT agent:\n{e}\nAddr: {addr}"


def _get_local_bt_address() -> str:
    import subprocess
    try:
        r = subprocess.run(["hciconfig", "hci0"], capture_output=True, text=True, timeout=5)
        for line in r.stdout.splitlines():
            if "BD Address" in line:
                return line.split()[2]
    except Exception:
        pass
    return "unknown"


def scan_bt_devices(is_debug: bool = False):
    """Return a list of nearby Bluetooth devices: [{'addr': str, 'name': str}]"""
    if is_debug:
        return [
            {"addr": "AA:BB:CC:DD:EE:FF", "name": "Debug Desktop"},
            {"addr": "11:22:33:44:55:66", "name": "Debug Device 2"},
        ]
    try:
        import bluetooth
        nearby = bluetooth.discover_devices(lookup_names=True, duration=8, flush_cache=True)
        return [{"addr": addr, "name": name or addr} for addr, name in nearby]
    except Exception as e:
        print(f"[BT] Scan error: {e}")
        return []


class BluetoothClient:
    def __init__(self, addr: str):
        self.addr = addr
        self._sock = None
        self._buf = ""

    def connect(self):
        import socket
        import bluetooth
        import re
        import sys
        # pybluez2 bug: is_valid_uuid missing in some builds.
        _uuid_pat = re.compile(
            r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
        )
        _is_valid_uuid = lambda u: bool(_uuid_pat.match(str(u).lower()))
        for _mod in sys.modules.values():
            if getattr(_mod, "__name__", "").startswith("bluetooth") and not hasattr(_mod, "is_valid_uuid"):
                _mod.is_valid_uuid = _is_valid_uuid
        try:
            services = bluetooth.find_service(uuid=BT_UUID, address=self.addr)
        except Exception as e:
            raise ConnectionError(f"SDP lookup failed: {e}") from e
        if not services:
            raise ConnectionError(
                "RekDeck service not found on this device.\n"
                "Make sure the desktop app is running as Administrator."
            )
        port = services[0]["port"]
        print(f"[BT] Connecting to {self.addr} on RFCOMM port {port}")
        # Use standard socket instead of pybluez2's BluetoothSocket — on BlueZ 5 the
        # raw pybluez2 socket bypasses the daemon and fails on paired devices.
        self._sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
        self._sock.connect((self.addr, port))

    def send(self, message: dict):
        if self._sock is None:
            self.connect()
        payload = json.dumps(message) + "\n"
        self._sock.send(payload.encode("utf-8"))

    def receive(self) -> dict:
        """Block until a complete newline-delimited JSON message arrives."""
        while "\n" not in self._buf:
            chunk = self._sock.recv(4096).decode("utf-8")
            if not chunk:
                raise ConnectionError("Bluetooth connection closed")
            self._buf += chunk
        line, self._buf = self._buf.split("\n", 1)
        return json.loads(line.strip())

    def close(self):
        if self._sock:
            try:
                self._sock.close()
            except Exception:
                pass
            self._sock = None
