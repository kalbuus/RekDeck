from kivy.uix.screenmanager import ScreenManager, Screen
from widgets.virtual_keyboard import VirtualKeyboard

class WifiPasswordScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.keyboard = VirtualKeyboard(self.ids.password_text_input, size_hint=(1, 0.6))
        self.add_widget(self.keyboard)