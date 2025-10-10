from kivy.uix.floatlayout import FloatLayout
from grid_widget import GridWidget
from deck_button import DeckButton

class DeckArea(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.7, 1)

        self.grid = GridWidget(cols=5, rows=3)
        self.add_widget(self.grid)

        # Активные кнопки на сетке
        self.active_buttons = []

        # Пример добавления кнопок из json (или вручную)
        self.add_deck_button(emoji="😀", hue=0.1, grid_x=0, grid_y=0, grid_w=1, grid_h=1)
        self.add_deck_button(emoji="✨", hue=0.4, grid_x=1, grid_y=0, grid_w=2, grid_h=1)
        self.add_deck_button(emoji="⭐", hue=0.6, grid_x=3, grid_y=1, grid_w=2, grid_h=2)

    def add_deck_button(self, **kwargs):
        btn = DeckButton(grid_widget=self.grid, **kwargs)
        self.add_widget(btn)
        self.active_buttons.append(btn)
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
