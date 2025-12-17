from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.app import App
from kivy.clock import Clock
import json

from interaction_managers.network_manager import *

class WifiConnectionScreen(Screen):
    show_popup = BooleanProperty()
    popup_text = StringProperty()
    def send_message(message):
        import asyncio
        layout = App.get_running_app().root.main_layout
        server = getattr(layout, 'server', None)
        if server is not None:
            loop = None
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                pass
            if loop and loop.is_running():
                asyncio.run_coroutine_threadsafe(server.send(message), loop)
    
    def __init__(self, **kwargs):
        self.show_popup = False
        self.popup_text = "Не удалось подключиться к сети"
        super().__init__(**kwargs)
    
    def on_enter(self, *args):
        self.try_connect()
    
    def try_connect(self):
        if is_connected():
            print("connecting")
            self.try_finding_server()
        else:
            App.get_running_app().sm.current = "wifi_select"

    def try_finding_server(self):
        """Ищем сервер в локальной сети и запускаем отдельный поток для WebSocket-клиента."""
        import threading, asyncio

        def ws_thread(server_ip):
            from kivy.app import App
            layout = App.get_running_app().root.main_layout
            layout.server = WebSocketClient(f"ws://{server_ip}:8765")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            async def ws_main():
                await layout.server.connect()
                while True:
                    try:
                        msg = await layout.server.receive()
                        if msg['cmd'] == "area_state":
                            Clock.schedule_once(lambda dt: layout.ids.deck_area_obj.load_preset_from_json(msg['data']))
                        else:
                            print(f"Unknown command: {msg['cmd']}")
                    except Exception as e:
                        print(f"WS error: {e}")
                        break
            # Сохраняем loop для дальнейших отправок
            layout._ws_loop = loop
            loop.run_until_complete(ws_main())

        def run_async():
            try:
                server_ip = asyncio.run(find_server_on_lan())
            except Exception:
                server_ip = None
            def update():
                if server_ip:
                    App.get_running_app().on_connect()
                    threading.Thread(target=ws_thread, args=(server_ip,), daemon=True).start()
                else:
                    self.popup_text = "Сервер не найден в локальной сети"
                self.show_popup = True
            Clock.schedule_once(lambda dt: update())
        threading.Thread(target=run_async, daemon=True).start()
        