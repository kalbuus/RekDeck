from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.animation import Animation

class DeckButton(Button):
    image_source = ObjectProperty(None)
    emoji = ObjectProperty(None)
    def get_hsv_color(self):
        # TODO: реализовать HSV-алгоритм, пока просто синий
        return (0.1, 0.6, 0.9, 1)
    grid_x = NumericProperty(0)
    grid_y = NumericProperty(0)
    grid_w = NumericProperty(1)
    grid_h = NumericProperty(1)
    selected = BooleanProperty(False)
    grid_widget = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.update_pos_size()

        self.dragging = False
        self.start_touch = None
        self.prev_grid_x = self.grid_x
        self.prev_grid_y = self.grid_y

        # Автоматически обновлять размер и позицию при изменении grid_widget
        if self.grid_widget:
            self._bind_to_grid_widget(self.grid_widget)

    def on_grid_widget(self, instance, value):
        # Если grid_widget меняется динамически
        self._bind_to_grid_widget(value)
        self.update_pos_size()

    def _bind_to_grid_widget(self, grid_widget):
        # Отписаться от предыдущего, если был
        if hasattr(self, '_grid_widget_binds'):
            for prop, uid in self._grid_widget_binds:
                grid_widget.unbind_uid(prop, uid)
        self._grid_widget_binds = []
        if grid_widget:
            for prop in ('width', 'height', 'cols', 'rows', 'pos', 'center_x', 'center_y'):
                uid = grid_widget.fbind(prop, self.update_pos_size)
                self._grid_widget_binds.append((prop, uid))

    def update_pos_size(self, *args):
        if not self.grid_widget or self.grid_widget.cols == 0:
            return
        cell_size = self.grid_widget.width / self.grid_widget.cols
        self.size = (self.grid_w * cell_size, self.grid_h * cell_size)
        px, py = self.grid_widget.grid_to_pixel(self.grid_x, self.grid_y)
        self.pos = (px, py)

    def _bring_to_front(self, dt):
        parent = self.parent
        if not parent:
            return
        try:
            parent.remove_widget(self)
            parent.add_widget(self)
        except Exception:
            pass

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.dragging = True
            self.start_touch = touch.pos
            self.prev_grid_x, self.prev_grid_y = self.grid_x, self.grid_y
            Clock.schedule_once(self._bring_to_front, 0)
            touch.grab(self)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self and self.dragging:
            dx = touch.pos[0] - self.start_touch[0]
            dy = touch.pos[1] - self.start_touch[1]
            self.x += dx
            self.y += dy
            self.start_touch = touch.pos
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            if self.dragging:
                self.dragging = False
                # Корректно вычисляем gx, gy относительно центра сетки
                grid = self.grid_widget
                cell_size = grid.width / grid.cols if grid.cols else 1
                grid_width = cell_size * grid.cols
                grid_height = cell_size * grid.rows
                left = grid.parent.center_x - grid_width / 2
                bottom = grid.parent.center_y - grid_height / 2
                gx = round((self.x - left) / cell_size)
                gy = round((self.y - bottom) / cell_size)

                parent = self.parent
                inside = self.grid_widget.inside_bounds(gx, gy, self.grid_w, self.grid_h)
                occupied = parent.check_collision(self, gx, gy, self.grid_w, self.grid_h) if parent else False

                if not inside or occupied:
                    tx, ty = self.grid_widget.grid_to_pixel(self.prev_grid_x, self.prev_grid_y)
                    anim = Animation(x=tx, y=ty, d=0.15, t='out_quad')
                    anim.start(self)
                    self.grid_x, self.grid_y = self.prev_grid_x, self.prev_grid_y
                    Clock.schedule_once(lambda dt: self.update_pos_size(), 0.16)
                else:
                    tx, ty = self.grid_widget.grid_to_pixel(gx, gy)

                    def _on_complete(anim, widget):
                        self.grid_x, self.grid_y = gx, gy
                        self.update_pos_size()

                    anim = Animation(x=tx, y=ty, d=0.12, t='out_quad')
                    anim.bind(on_complete=_on_complete)
                    anim.start(self)
                return True
        return super().on_touch_up(touch)
