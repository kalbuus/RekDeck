from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.lang.builder import Builder
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

class MainLayout(BoxLayout):
    overlay_menu = ObjectProperty(None, allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.overlay_menu = None

    def show_category_menu(self):
        import json
        if self.overlay_menu is None:
            json_path = os.path.join(os.path.dirname(__file__), 'button_types.json')
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            categories = []
            for cat in data:
                categories.append({
                    'name': cat['category'],
                    'types': [
                        btn.get('display_name') or 
                        btn.get('emoji') or 
                        btn.get('icon') or 
                        btn.get('script') or ''
                        for btn in cat.get('buttons', [])
                    ]
                })
            self.overlay_menu = ButtonCategoryMenu(categories=categories)
            self.overlay_menu.bind(on_dismiss=self._on_menu_dismiss)
        self.overlay_menu.open()

    def _on_menu_dismiss(self, *args):
        self.overlay_menu = None

class MainApp(App):
    def build(self):
        self.layout = MainLayout()
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
        return self.layout

if __name__ == "__main__":
    MainApp().run()
