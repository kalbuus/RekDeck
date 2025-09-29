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

class MainLayout(BoxLayout):
    pass

class MainApp(App):
    def build(self):
        return MainLayout()


if __name__ == "__main__":
    MainApp().run()
