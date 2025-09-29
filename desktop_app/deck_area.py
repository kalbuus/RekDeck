from kivy.uix.floatlayout import FloatLayout
from grid_widget import GridWidget
from deck_button import DeckButton

CELL_SIZE = 100  # размер одной ячейки сетки

class DeckArea(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.7, 1)

        self.grid = GridWidget(cols=5, rows=3, cell_size=CELL_SIZE, pos_hint={"center_x":0.6, "center_y":0.8})
        self.add_widget(self.grid)

        self.add_widget(DeckButton(text="1x1", grid_x=5, grid_y=5, grid_w=1, grid_h=1, grid_widget=self.grid))
        self.add_widget(DeckButton(text="1x2", grid_x=5, grid_y=5, grid_w=2, grid_h=1, grid_widget=self.grid))
        self.add_widget(DeckButton(text="2x2", grid_x=5, grid_y=5, grid_w=2, grid_h=2, grid_widget=self.grid))

    def check_collision(self, btn, gx, gy, gw, gh):
        for child in self.children:
            if isinstance(child, DeckButton) and child is not btn:
                if (gx < child.grid_x + child.grid_w and
                    gx + gw > child.grid_x and
                    gy < child.grid_y + child.grid_h and
                    gy + gh > child.grid_y):
                    return True
        return False
