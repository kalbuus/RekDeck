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
            # Ожидаем, что ssid и пароль заданы извне перед вызовом
            # если их нет — показываем экран выбора
            pass
    
    def try_connecting_to_wifi(self, ssid, password):
        """Пытаемся подключиться к WiFi и показываем результат во всплывающем окне."""
        success, msg = connect_wifi(ssid, password)
        if success:
            self.popup_text = f"Подключено к {ssid}"
            self.show_popup = True
            # После подключения пробуем найти сервер
            server_ip = find_server_on_lan()
            if server_ip:
                self.popup_text = f"Найден сервер: {server_ip}"
            else:
                self.popup_text = "Подключено, но сервер не найден"
            self.show_popup = True
        else:
            self.popup_text = f"Ошибка подключения: {msg}"
            self.show_popup = True

    def try_finding_server(self):
        """Ищем сервер в локальной сети и обновляем popup_text."""
        server_ip = find_server_on_lan()
        if server_ip:
            self.popup_text = f"Найден сервер: {server_ip}"
            self.show_popup = True
        else:
            self.popup_text = "Сервер не найден в локальной сети"
            self.show_popup = True