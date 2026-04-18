#from kivy.config import Config
#Config.set('modules', 'cursor', '0')

from kivy.core.window import Window
Window.show_cursor = False

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivy.factory import Factory
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty

from screens.wifi_select_screen import WifiSelectScreen
from screens.wifi_password_screen import WifiPasswordScreen
from screens.wifi_connection_screen import WifiConnectionScreen
from screens.connection_select_screen import ConnectionSelectScreen
from screens.bt_connection_screen import BtConnectionScreen
from widgets.networks_recycle_view import NetworksRecycleView, SelectableNetworkLabel
from widgets.virtual_keyboard import VirtualKeyboard, KeyboardButton
from interaction_managers.network_manager import WebSocketClient
from widgets.deck_area import DeckArea
from interaction_managers.network_manager import is_connected

import asyncio
import os

Window.size = (800,480)

class BaseFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.main_layout = self.ids.main_layout

class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        self.server = None
        super().__init__(**kwargs)

class WifiLayout(BoxLayout):
    pass

kv_file_count = 0
for _kv_root, _, _kv_files in os.walk(os.getcwd()):
    for _kv_file in _kv_files:
        if _kv_file.endswith(".kv") and "desktop_app" not in _kv_root:
            _kv_path = os.path.join(_kv_root, _kv_file)
            try:
                Builder.load_file(_kv_path)
                kv_file_count += 1
            except Exception as _kv_err:
                print(f"[KV ERROR] {_kv_path}: {_kv_err}")

print(f"Found and loaded {kv_file_count} .kv files!")

class StreamDeckApp(App):
    is_debug_mode = os.name == 'nt' # Debug mode on windows only
    wifi_current_ssid = StringProperty()
    wifi_current_has_password = BooleanProperty()
    wifi_current_password = StringProperty()
    sm = ObjectProperty()

    def build(self):
        import os, glob
        assets_dir = os.path.join(os.getcwd(), "assets")
        for tmp_img in glob.glob(os.path.join(assets_dir, "temp_*.png")):
            try:
                os.remove(tmp_img)
            except Exception:
                pass

        if not self.is_debug_mode: Window.fullscreen = True
        self.root = BaseFloatLayout()

        self.sm = self.root.ids.wifi_screen_manager

        self.sm.add_widget(Factory.ConnectionSelectScreen(name="connection_select"))
        self.sm.add_widget(Factory.WifiSelectScreen(name="wifi_select"))
        self.sm.add_widget(Factory.WifiPasswordScreen(name="wifi_password"))
        self.sm.add_widget(Factory.WifiConnectionScreen(name="wifi_connect"))
        self.sm.add_widget(Factory.BtConnectionScreen(name="bt_connect"))

        self.sm.current = "connection_select"
        return self.root
    
    def on_start(self):
        from kivy.clock import Clock
        from kivy.core.window import Window
        Clock.schedule_once(lambda _: Window.canvas.ask_update(), 0.5)

    def on_connect(self):
        self.root.remove_widget(self.root.ids.wifi_layout)

    def on_disconnect(self):
        self.root.add_widget(self.root.ids.wifi_layout)
        self.sm.current = "connection_select"


def main():
    asyncio.run(StreamDeckApp().async_run(async_lib="asyncio"))


if __name__ == '__main__':
    main()