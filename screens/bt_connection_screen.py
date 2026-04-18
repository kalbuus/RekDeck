import threading

from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty, ListProperty
from kivy.app import App
from kivy.clock import Clock

from interaction_managers.bluetooth_manager import scan_bt_devices, BluetoothClient


class BtConnectionScreen(Screen):
    is_scanning = BooleanProperty(False)
    show_popup = BooleanProperty(False)
    popup_text = StringProperty("")
    devices = ListProperty([])  # list of {'addr': str, 'name': str}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def on_enter(self, *args):
        self.show_popup = False
        self.devices = []
        self.start_scan()

    def start_scan(self):
        self.is_scanning = True
        self.devices = []
        is_debug = __import__("os").name == "nt"
        threading.Thread(target=self._scan_thread, args=(is_debug,), daemon=True).start()

    def _scan_thread(self, is_debug):
        found = scan_bt_devices(is_debug=is_debug)
        Clock.schedule_once(lambda dt: self._on_scan_done(found))

    def _on_scan_done(self, found):
        self.is_scanning = False
        if found:
            self.devices = found
            self._populate_device_list()
        else:
            self.popup_text = "Устройства не найдены"
            self.show_popup = True

    def _populate_device_list(self):
        from kivy.uix.button import Button
        device_list = self.ids.device_list
        device_list.clear_widgets()
        for dev in self.devices:
            addr = dev["addr"]
            name = dev["name"]
            btn = Button(
                text=f"{name}\n{addr}",
                size_hint_y=None,
                height=70,
                font_size=18,
                halign="center",
            )
            btn.bind(on_release=lambda inst, a=addr, n=name: self.connect_to_device(a, n))
            device_list.add_widget(btn)

    def connect_to_device(self, addr, name):
        self.show_popup = False
        self.is_scanning = True
        threading.Thread(target=self._connect_thread, args=(addr, name), daemon=True).start()

    def _connect_thread(self, addr, name):
        client = BluetoothClient(addr)
        try:
            client.connect()
        except Exception as e:
            err = str(e)
            Clock.schedule_once(lambda dt, msg=err: self._on_connect_fail(msg))
            return

        Clock.schedule_once(lambda dt: self._on_connect_success(client))
        self._run_message_loop(client)

    def _on_connect_success(self, client):
        self.is_scanning = False
        layout = App.get_running_app().root.main_layout
        layout.server = client
        App.get_running_app().on_connect()

    def _on_connect_fail(self, error):
        self.is_scanning = False
        self.popup_text = f"Не удалось подключиться:\n{error}"
        self.show_popup = True

    def _run_message_loop(self, client):
        while True:
            try:
                msg = client.receive()
                cmd = msg.get("cmd")
                if cmd == "area_state":
                    layout = App.get_running_app().root.main_layout
                    Clock.schedule_once(
                        lambda dt, d=msg["data"]: layout.ids.deck_area_obj.load_preset_from_json(d)
                    )
                else:
                    print(f"[BT] Unknown command: {cmd}")
            except Exception as e:
                print(f"[BT] Connection lost: {e}")
                Clock.schedule_once(lambda dt: App.get_running_app().on_disconnect())
                break

    def go_back(self):
        App.get_running_app().sm.current = "connection_select"
