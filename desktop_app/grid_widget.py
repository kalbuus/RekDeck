
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Line

class GridWidget(Widget):
    cols = NumericProperty(8)
    rows = NumericProperty(5)
    cell_size = NumericProperty(100)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_grid,
                  size=self.update_grid,
                  cols=self.update_grid,
                  rows=self.update_grid)

    def update_grid(self, *args):
        """Просто перерисовывает сетку без изменения размеров виджета"""
        self.canvas.clear()
        if self.cols <= 0 or self.rows <= 0:
            return

        # Расчёт размера клетки, чтобы сетка влезла по ширине
        cell_size = self.width / self.cols
        grid_width = cell_size * self.cols
        grid_height = cell_size * self.rows

        # Центрируем сетку внутри виджета
        left = self.x + (self.width - grid_width) / 2
        bottom = self.y + (self.height - grid_height) / 2

        with self.canvas:
            Color(0.365, 0.384, 0.565, 1)
            for x in range(self.cols + 1):
                px = left + x * cell_size
                Line(points=[px, bottom, px, bottom + grid_height], width=1)
            for y in range(self.rows + 1):
                py = bottom + y * cell_size
                Line(points=[left, py, left + grid_width, py], width=1)

    def grid_to_pixel(self, gx, gy):
        """Перевод координат клетки в пиксели относительно текущей сетки"""
        if self.cols <= 0 or self.rows <= 0:
            return self.center

        cell_size = self.width / self.cols
        grid_width = cell_size * self.cols
        grid_height = cell_size * self.rows
        left = self.x + (self.width - grid_width) / 2
        bottom = self.y + (self.height - grid_height) / 2
        return (left + gx * cell_size, bottom + gy * cell_size)

    def inside_bounds(self, gx, gy, gw, gh):
        return 0 <= gx and 0 <= gy and gx + gw <= self.cols and gy + gh <= self.rows
