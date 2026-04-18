from kivy.uix.screenmanager import Screen
from kivy.app import App

from interaction_managers.network_manager import is_connected


class ConnectionSelectScreen(Screen):
    def go_wifi(self):
        app = App.get_running_app()
        if is_connected():
            app.sm.current = "wifi_connect"
        else:
            app.sm.current = "wifi_select"

    def go_bluetooth(self):
        App.get_running_app().sm.current = "bt_connect"
