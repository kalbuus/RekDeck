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
for root, _, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".kv") and "desktop_app" not in root:
            divider = "\\" if os.name == 'nt' else '/'
            Builder.load_file(root + divider + file)
            kv_file_count += 1

print(f"Found and loaded {kv_file_count} .kv files!")

class StreamDeckApp(App):
    is_debug_mode = os.name == 'nt' # Debug mode on windows only
    wifi_current_ssid = StringProperty()
    wifi_current_has_password = BooleanProperty()
    wifi_current_password = StringProperty()
    sm = ObjectProperty()

    def build(self):
        if not self.is_debug_mode: Window.fullscreen = True
        self.root = BaseFloatLayout()

        self.sm = self.root.ids.wifi_screen_manager

        connected = is_connected()
        
        if not connected:
            self.sm.add_widget(Factory.WifiSelectScreen(name="wifi_select"))
            self.sm.add_widget(Factory.WifiPasswordScreen(name="wifi_password"))
            self.sm.add_widget(Factory.WifiConnectionScreen(name="wifi_connect"))
        else:
            self.sm.add_widget(Factory.WifiConnectionScreen(name="wifi_connect"))
            self.sm.add_widget(Factory.WifiPasswordScreen(name="wifi_password"))
            self.sm.add_widget(Factory.WifiSelectScreen(name="wifi_select"))
        
        starting_page = "wifi_connect" if connected else "wifi_select"
        
        self.sm.current = starting_page
        return self.root
    
    def on_connect(self):
        self.root.remove_widget(self.root.ids.wifi_layout)
        


def main():
    asyncio.run(StreamDeckApp().async_run(async_lib="asyncio"))


if __name__ == '__main__':
    main()