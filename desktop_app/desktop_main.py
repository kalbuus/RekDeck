from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang.builder import Builder
from threading import Thread
import pystray
from PIL import Image
import os
kv_file_count = 0
desktop_kv_dir = os.path.join(os.path.dirname(__file__))
for root, _, files in os.walk(desktop_kv_dir):
    for file in files:
        if file.endswith(".kv"):
            Builder.load_file(os.path.join(root, file))
            kv_file_count += 1
print(f"Found and loaded {kv_file_count} .kv files in desktop_app.")

from grid_widget import GridWidget
from deck_button import DeckButton
from deck_area import DeckArea
from animated_plus_button import AnimatedPlusButton
from button_category_menu import ButtonCategoryMenu

from button_types_util import buttonTypesUtilInstance
from ws_server import WsServer

class MainLayout(BoxLayout):
    @property
    def app(self):
        from kivy.app import App
        return App.get_running_app()

    def get_last_selected_button(self):
        return self.app.get_last_selected_button()
    overlay_menu = ObjectProperty(None, allownone=True)
    deck_area = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlay_menu = None

    def show_category_menu(self):
        if self.overlay_menu is None:
            categories = buttonTypesUtilInstance.get_categories()
            self.overlay_menu = ButtonCategoryMenu(categories=categories)
            self.overlay_menu.bind(on_dismiss=self._on_menu_dismiss)
        self.overlay_menu.open()

    def _on_menu_dismiss(self, *args):
        self.overlay_menu = None

class AppIcon(pystray.Icon):
    def __init__(self, app, name, icon=None, title=None, menu=None, **kwargs):
        super().__init__(name, icon, title, menu, **kwargs)
        self.kvApp = app

    def _on_notify(self, wparam, lparam):
        super()._on_notify(wparam, lparam)
        if (hex(lparam) == "0x202"):
            self.kvApp.show_window("", "")
            print("Mouse Button Pressed")

class MainApp(App):
    last_selected_button = ObjectProperty(None)
    layout = None

    def set_last_selected_button(self, btn):
        self.last_selected_button = btn
        self.update_settings()
    
    def update_settings(self):
        if self.last_selected_button == None: return
        self.layout.ids.hue_slider.value = self.last_selected_button.hue

    def get_last_selected_button(self):
        return self.last_selected_button
    
    def build(self):
        self.layout = MainLayout()
        # Запускаем WebSocket сервер
        self.ws_server = WsServer(host='0.0.0.0', port=8765, app=self)
        try:
            self.ws_server.start()
        except Exception as e:
            print('Failed to start ws server:', e)
        self.tray_icon = None
        Window.bind(on_request_close=self.on_request_close)
        # Найти плюс-кнопку и добавить обработчик
        def on_plus(instance):
            self.layout.show_category_menu()
            Clock.schedule_once(lambda dt: _bind_x(self.layout), 0)
        def on_x(instance):
            self.layout.overlay_menu.dismiss()
        # Ждем, пока layout построится полностью
        Clock.schedule_once(lambda dt: _bind_plus(self.layout), 0)
        def _bind_plus(layout):
            # Ищем AnimatedPlusButton внутри layout
            for child in layout.walk():
                if isinstance(child, AnimatedPlusButton):
                    child.bind(on_release=lambda inst: on_plus(inst))
        def _bind_x(layout):
            if(layout.overlay_menu == None):
                return
            for child in layout.overlay_menu.walk():
                if isinstance(child, AnimatedPlusButton):
                    child.bind(on_release=lambda inst: on_x(inst))
        Thread(target=self.create_tray_icon, daemon=True).start()
        return self.layout
    
    def on_request_close(self, *args):
        """Перехватываем закрытие окна"""
        Window.hide()
        return True  # не даём приложению закрыться

    def get_deck_area(self):
        if self.layout != None:
            return self.layout.deck_area
        else:
            return None
    
    def create_tray_icon(self):
        """Создаём иконку в системном трее"""
        # Создаём иконку
        with Image.open(r"assets/python.ico") as icon_image:
            self.tray_icon = AppIcon(self, "name", icon_image, "Title", [
                pystray.MenuItem("Показать окно", self.show_window),
                pystray.MenuItem("Выход", self.quit_app)])

        # Запускаем иконку
        self.tray_icon.run_detached()

    def show_window(self, icon, item):
        """Показать окно"""
        Clock.schedule_once(lambda dt: Window.show())
        Clock.schedule_once(lambda dt: Window.raise_window())

    def quit_app(self, icon, item):
        # Завершить приложение полностью
        try:
            if hasattr(self, 'ws_server') and self.ws_server:
                self.ws_server.stop()
        except Exception:
            pass
        icon.stop()
        self.stop()

if __name__ == "__main__":
    MainApp().run()
