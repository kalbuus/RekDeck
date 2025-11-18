from kivy.uix.screenmanager import ScreenManager, Screen
from widgets.virtual_keyboard import VirtualKeyboard
from kivy.uix.button import Button
from kivy.app import App
from interaction_managers import network_manager

class WifiPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.keyboard = VirtualKeyboard(self.ids.password_text_input, size_hint=(1, 0.6))
        self.add_widget(self.keyboard)

        self.done_button = DoneButton(
            text="Done", 
            on_press=self.on_done, 
            size_hint=(0.2, 0.1), 
            pos_hint={'center_x': 0.85, 'center_y': 0.87})
        
        self.add_widget(self.done_button)
    
    def on_done(self, instance):
        app = App.get_running_app()
        app.wifi_current_password = self.ids.password_text_input.text
        network_manager.connect_wifi(app.wifi_current_ssid, app.wifi_current_password)
        
        sm = app.root.ids.wifi_screen_manager
        sm.current = "wifi_connect"


class DoneButton(Button):
    pass