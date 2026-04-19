import json
import queue
import threading
import copy
import base64
import os

from deck_area import CONFIG_PATH
from kivy.app import App

BT_UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
BT_SERVICE_NAME = "RekDeck"


class BtServer:
    def __init__(self, app=None):
        self.app = app
        self._server_sock = None
        self._clients = []
        self._clients_lock = threading.Lock()
        self._thread = None
        self._running = False
        self.event_queue = queue.Queue()

    def encode_data(self, data):
        result = copy.deepcopy(data)
        for i in result:
            icon_path = i.get("icon", "")
            if icon_path:
                abs_path = os.path.join("assets", icon_path)
                try:
                    with open(abs_path, "rb") as img_file:
                        b64_icon = base64.b64encode(img_file.read()).decode("utf-8")
                    i["icon"] = b64_icon
                except Exception:
                    i["icon"] = ""
            else:
                i["icon"] = ""
        return result

    def _broadcast_loop(self):
        import time
        while self._running:
            if not self.event_queue.empty():
                event = self.event_queue.get()
                self._send_raw_to_all(event)
            time.sleep(0.1)

    def _send_raw_to_all(self, payload: str):
        data = (payload + "\n").encode("utf-8")
        with self._clients_lock:
            for sock in self._clients[:]:
                try:
                    sock.send(data)
                except Exception:
                    try:
                        self._clients.remove(sock)
                    except ValueError:
                        pass

    def _handle_client(self, client_sock):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                preset = self.encode_data(json.load(f))
        except Exception:
            preset = {}
        try:
            msg = json.dumps({"cmd": "area_state", "data": preset}) + "\n"
            client_sock.send(msg.encode("utf-8"))
        except Exception:
            return

        buf = ""
        while self._running:
            try:
                chunk = client_sock.recv(4096).decode("utf-8")
                if not chunk:
                    break
                buf += chunk
                while "\n" in buf:
                    line, buf = buf.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        data = json.loads(line)
                    except Exception:
                        continue
                    cmd = data.get("cmd")
                    if cmd == "button_press":
                        idx = data.get("data")
                        try:
                            from kivy.clock import Clock
                            Clock.schedule_once(
                                lambda dt, i=idx: App.get_running_app().layout.deck_area.press_button_by_index(i)
                            )
                        except Exception as e:
                            print(f"[BtServer] button_press error: {e}")
            except Exception:
                break

        with self._clients_lock:
            try:
                self._clients.remove(client_sock)
            except ValueError:
                pass
        try:
            client_sock.close()
        except Exception:
            pass

    def _enable_discoverability(self):
        try:
            import ctypes
            bthprops = ctypes.WinDLL("bthprops.cpl")
            bthprops.BluetoothEnableDiscovery(None, True)
            print("[BtServer] Windows Bluetooth discoverability enabled.")
        except Exception as e:
            print(f"[BtServer] Could not enable discoverability: {e}")

    def _run(self):
        try:
            import bluetooth
        except ImportError:
            print("[BtServer] pybluez2 not installed. Bluetooth server unavailable.")
            return

        self._enable_discoverability()

        try:
            self._server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self._server_sock.bind(("", bluetooth.PORT_ANY))
            self._server_sock.listen(5)
            port = self._server_sock.getsockname()[1]
            print(f"[BtServer] Socket bound on RFCOMM port {port}")
        except Exception as e:
            print(f"[BtServer] Failed to create socket: {e}")
            return

        try:
            bluetooth.advertise_service(
                self._server_sock,
                BT_SERVICE_NAME,
                service_id=BT_UUID,
                service_classes=[BT_UUID, bluetooth.SERIAL_PORT_CLASS],
                profiles=[bluetooth.SERIAL_PORT_PROFILE],
            )
            print(f"[BtServer] SDP service advertised, UUID={BT_UUID}")
        except Exception as e:
            print(f"[BtServer] SDP advertisement failed — Pi won't be able to connect. "
                  f"Try running as Administrator. Error: {e}")

        print(f"[BtServer] Listening on RFCOMM port {port}")

        self._running = True
        threading.Thread(target=self._broadcast_loop, daemon=True).start()

        while self._running:
            try:
                client_sock, addr = self._server_sock.accept()
                print(f"[BtServer] Client connected: {addr}")
                with self._clients_lock:
                    self._clients.append(client_sock)
                threading.Thread(
                    target=self._handle_client, args=(client_sock,), daemon=True
                ).start()
            except Exception:
                break

    def start(self):
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._server_sock:
            try:
                self._server_sock.close()
            except Exception:
                pass
        with self._clients_lock:
            for sock in self._clients[:]:
                try:
                    sock.close()
                except Exception:
                    pass
            self._clients.clear()

    def send_to_all(self, message: dict):
        payload = json.dumps(message)
        self._send_raw_to_all(payload)
