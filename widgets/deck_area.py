from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.properties import ListProperty

from widgets.deck_button import DeckButton
from widgets.grid_widget import GridWidget

import colorsys

class DeckArea(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Внутренняя сетка для отображения ячеек
        self.grid = GridWidget(cols=5, rows=3)
        self.add_widget(self.grid)

        # Список активных (визуальных) кнопок
        self.active_buttons = []

        # Примеры кнопок (визуализация)
        self.add_deck_button(emoji="😀", hue=0.1, grid_x=0, grid_y=0, grid_w=1, grid_h=1)
        self.add_deck_button(emoji="✨", hue=0.4, grid_x=1, grid_y=0, grid_w=2, grid_h=1)
        self.add_deck_button(emoji="⭐", hue=0.6, grid_x=3, grid_y=1, grid_w=2, grid_h=2)

    def _hsv_to_rgba(self, h, s=0.4, v=0.8):
        r,g,b = colorsys.hsv_to_rgb(h, s, v)
        return (r, g, b, 1)

    def add_deck_button(self, **kwargs):
        btn = DeckButton(grid_widget=self.grid, **kwargs)
        self.add_widget(btn)
        self.active_buttons.append(btn)
        return btn
