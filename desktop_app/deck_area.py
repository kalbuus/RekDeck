from kivy.uix.floatlayout import FloatLayout
from grid_widget import GridWidget
from deck_button import DeckButton

CONFIG_PATH = r"preset.json"

class DeckArea(FloatLayout):
    def save_buttons_to_json(self):
        import json
        data = []
        for btn in self.active_buttons:
            btn_data = {
                'id': getattr(btn, 'button_id', None),
                'hue': btn.hue,
                'grid_x': btn.grid_x,
                'grid_y': btn.grid_y,
                'grid_w': btn.grid_w,
                'grid_h': btn.grid_h
            }
            data.append(btn_data)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_buttons_from_json(self, button_types_util=None):
        import json
        if button_types_util is None:
            from button_types_util import buttonTypesUtilInstance
            button_types_util = buttonTypesUtilInstance
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
            btn_id = btn_data.get('id')
            btn_info = None
            # Поиск информации о кнопке по id во всех категориях
            for i in button_types_util.get_categories():
                if btn_id in i["types"]:
                    btn_info = button_types_util.get_button_info(i["id"], btn_id)
                if btn_info:
                    break
            if not btn_info:
                continue
            # Создаём DeckButton с нужными параметрами
            kwargs = {
                'hue': btn_data.get('hue', 0.1),
                'grid_x': btn_data.get('grid_x', 0),
                'grid_y': btn_data.get('grid_y', 0),
                'grid_w': btn_data.get('grid_w', 1),
                'grid_h': btn_data.get('grid_h', 1),
                'emoji': btn_info.get('emoji', ''),
                'image_source': btn_info.get('icon', ''),
            }
            btn = DeckButton(grid_widget=self.grid, **kwargs)
            btn.button_id = btn_id
            self.add_widget(btn)
            self.active_buttons.append(btn)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.7, 1)

        self.grid = GridWidget(cols=5, rows=3)
        self.add_widget(self.grid)

        # Активные кнопки на сетке
        self.active_buttons = []
        self.load_buttons_from_json()
        
        #self.add_deck_button(emoji="😀", hue=0.1, grid_x=0, grid_y=0, grid_w=1, grid_h=1)
        #self.add_deck_button(emoji="✨", hue=0.4, grid_x=1, grid_y=0, grid_w=2, grid_h=1)
        #self.add_deck_button(emoji="⭐", hue=0.6, grid_x=3, grid_y=1, grid_w=2, grid_h=2)

    def add_deck_button(self, **kwargs):
        btn = DeckButton(grid_widget=self.grid, **kwargs)
        self.add_widget(btn)
        self.active_buttons.append(btn)
        self.save_buttons_to_json()
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
