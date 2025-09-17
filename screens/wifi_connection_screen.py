from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, StringProperty

from interaction_managers.network_manager import *

class WifiConnectionScreen(Screen):
    show_popup = BooleanProperty()
    popup_text = StringProperty()
    def __init__(self, **kwargs):
        self.show_popup = False
        self.popup_text = "Не удалось подключиться к сети"
        super().__init__(**kwargs)
    
    def on_enter(self, *args):
        if is_connected():
            self.try_finding_server()
        else:
            self.try_connecting_to_wifi()
    
    def try_connecting_to_wifi(self, ssid, password):
        print("connecting")
    
    def try_finding_server(self):
        print("finding")