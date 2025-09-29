from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Line

CELL_SIZE = 100  # размер одной ячейки сетки

class GridWidget(Widget):
    cols = NumericProperty(8)
    rows = NumericProperty(5)
    cell_size = NumericProperty(CELL_SIZE)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_grid,
                  size=self.update_grid,
                  cols=self.update_grid,
                  rows=self.update_grid,
                  cell_size=self.update_grid)

    def update_grid(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.3, 0.3, 0.3, 0.3)
            for x in range(self.cols + 1):
                px = self.x + x * self.cell_size
                Line(points=[px, self.y, px, self.y + self.rows * self.cell_size], width=1)
            for y in range(self.rows + 1):
                py = self.y + y * self.cell_size
                Line(points=[self.x, py, self.x + self.cols * self.cell_size, py], width=1)

    def grid_to_pixel(self, gx, gy):
        return (self.x + gx * self.cell_size, self.y + gy * self.cell_size)

    def inside_bounds(self, gx, gy, gw, gh):
        if gx < 0 or gy < 0:
            return False
        if gx + gw > self.cols or gy + gh > self.rows:
            return False
        return True
