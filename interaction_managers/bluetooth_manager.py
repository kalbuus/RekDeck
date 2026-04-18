import json
import os

BT_UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"


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
        import bluetooth
        services = bluetooth.find_service(uuid=BT_UUID, address=self.addr)
        if not services:
            raise ConnectionError(f"RekDeck service not found on {self.addr}")
        port = services[0]["port"]
        self._sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
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
