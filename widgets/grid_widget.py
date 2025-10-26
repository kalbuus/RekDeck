
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Line

class GridWidget(Widget):
    cols = NumericProperty(8)
    rows = NumericProperty(5)
    cell_size = NumericProperty(100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._last_width = None
        self._last_cols = None
        self._last_rows = None
        self.bind(pos=self.update_grid,
                  width=self._on_width_or_grid,
                  cols=self._on_width_or_grid,
                  rows=self._on_width_or_grid)

    def _on_width_or_grid(self, *args):
        # Высота пересчитывается только если реально изменилась ширина, cols или rows
        if self.cols == 0:
            return
        cell_size = self.width / self.cols
        new_height = cell_size * self.rows
        if self.height != new_height:
            self.height = new_height
        self.update_grid()

    def update_grid(self, *args):
        self.canvas.clear()
        if self.cols == 0:
            return
        
        cell_size = self.width / self.cols
        grid_width = cell_size * self.cols
        grid_height = cell_size * self.rows
        # Центрируем сетку относительно центра виджета
        left = self.parent.center_x - grid_width / 2
        bottom = self.parent.center_y - grid_height / 2
        with self.canvas:
            Color(0.365, 0.384, 0.565, 0.2)
            for x in range(self.cols + 1):
                px = left + x * cell_size
                Line(points=[px, bottom, px, bottom + grid_height], width=1)
            for y in range(self.rows + 1):
                py = bottom + y * cell_size
                Line(points=[left, py, left + grid_width, py], width=1)

    def grid_to_pixel(self, gx, gy):
        if self.cols == 0:
            return (self.parent.center_x, self.parent.center_y)
        cell_size = self.width / self.cols
        grid_width = cell_size * self.cols
        grid_height = cell_size * self.rows
        left = self.parent.center_x - grid_width / 2
        bottom = self.parent.center_y - grid_height / 2
        return (left + gx * cell_size, bottom + gy * cell_size)

    def inside_bounds(self, gx, gy, gw, gh):
        if gx < 0 or gy < 0:
            return False
        if gx + gw > self.cols or gy + gh > self.rows:
            return False
        return True
