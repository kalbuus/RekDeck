from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.app import App

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
            # Ожидаем, что ssid и пароль заданы извне перед вызовом
            # если их нет — показываем экран выбора
            App.get_running_app().sm.current = "wifi_select"

    def try_finding_server(self):
        """Ищем сервер в локальной сети асинхронно и обновляем popup_text через callback."""
        import threading, asyncio
        def run_async():
            try:
                server_ip = asyncio.run(find_server_on_lan())
            except Exception:
                server_ip = None
            def update():
                if server_ip:
                    self.popup_text = f"Найден сервер: {server_ip}"
                else:
                    self.popup_text = "Сервер не найден в локальной сети"
                self.show_popup = True
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: update())
        threading.Thread(target=run_async, daemon=True).start()