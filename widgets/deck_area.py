from kivy.uix.floatlayout import FloatLayout
from widgets.deck_button import DeckButton
from widgets.grid_widget import GridWidget

import colorsys

CONFIG_PATH = r"preset.json"

class DeckArea(FloatLayout):
    def load_preset_from_json(self, data):
        # Удаляем старые кнопки
        for btn in list(self.active_buttons):
            self.remove_widget(btn)
        self.active_buttons.clear()
        # Добавляем новые
        for btn_data in data:
            btn_info = None
            kwargs = {
                'button_id': btn_data.get('id'),
                'hue': btn_data.get('hue', 0.1),
                'grid_x': btn_data.get('grid_x', 0),
                'grid_y': btn_data.get('grid_y', 0),
                'grid_w': btn_data.get('grid_w', 1),
                'grid_h': btn_data.get('grid_h', 1),
                'image_source': btn_data.get('icon', ''),
            }
            btn = DeckButton(grid_widget=self.grid, **kwargs)
            self.add_widget(btn)
            self.active_buttons.append(btn)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.7, 1)
        self.last_index = 0

        self.grid = GridWidget(cols=5, rows=3, pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.add_widget(self.grid)

        # Активные кнопки на сетке
        self.active_buttons = []

    def add_deck_button(self, **kwargs):
        btn = DeckButton(grid_widget=self.grid, **kwargs)
        self.add_widget(btn)
        self.active_buttons.append(btn)
        self.save_preset_to_json()
        return btn

