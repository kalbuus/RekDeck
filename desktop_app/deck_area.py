from kivy.uix.floatlayout import FloatLayout
from grid_widget import GridWidget
from deck_button import DeckButton

from kivy.app import App

CONFIG_PATH = r"preset.json"

class DeckArea(FloatLayout):
    def save_preset_to_json(self):
        import json
        data = []
        for btn in self.active_buttons:
            if btn.index == 0: # не изменённое значение
                continue
            btn_data = {
                'id': getattr(btn, 'button_id', None),
                'index': btn.index,
                'hue': btn.hue,
                'icon': btn.image_source,
                'grid_x': btn.grid_x,
                'grid_y': btn.grid_y,
                'grid_w': btn.grid_w,
                'grid_h': btn.grid_h,
            }
            data.append(btn_data)
        
        server = App.get_running_app().ws_server

        if server:
            server.send_to_all({'cmd': "area_state", 'data': data})
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_preset_from_json(self):
        import json
        try:
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            self.save_buttons_to_json() # Создаём пустой json если не нашли нужный
            return
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

        self.grid = GridWidget(cols=5, rows=3, pos_hint={"center_x": 0.5, "center_y": 0.5}, deck_area=self)
        self.add_widget(self.grid)

        # Активные кнопки на сетке
        self.active_buttons = []
        #self.load_buttons_from_json()
    
    def get_next_index(self):
        self.last_index += 1
        return self.last_index

    def add_deck_button(self, **kwargs):
        btn = DeckButton(grid_widget=self.grid, **kwargs)
        self.add_widget(btn)
        self.active_buttons.append(btn)
        self.save_preset_to_json()
        return btn

    def check_collision(self, btn, gx, gy, gw, gh):
        for b in self.active_buttons:
            if b is btn:
                continue
            if (gx < b.grid_x + b.grid_w and
                gx + gw > b.grid_x and
                gy < b.grid_y + b.grid_h and
                gy + gh > b.grid_y):
                return True
        return False

    def find_first_free_spot(self, size_x, size_y):
        """
        Находит первое свободное место для кнопки размера size_x x size_y.
        Возвращает (gx, gy) или None, если не найдено.
        """
        cols = self.grid.cols
        rows = self.grid.rows
        for gy in range(rows - size_y + 1):
            for gx in range(cols - size_x + 1):
                # Проверяем пересечение с уже размещёнными кнопками
                collision = False
                for b in self.active_buttons:
                    if (gx < b.grid_x + b.grid_w and
                        gx + size_x > b.grid_x and
                        gy < b.grid_y + b.grid_h and
                        gy + size_y > b.grid_y):
                        collision = True
                        break
                if not collision:
                    return (gx, gy)
        return None
