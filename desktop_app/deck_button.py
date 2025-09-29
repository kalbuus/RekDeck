from kivy.uix.button import Button
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.animation import Animation

class DeckButton(Button):
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

        with self.canvas.before:
            Color(0.1, 0.6, 0.9, 1 if self.selected else 0.8)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_graphics, size=self.update_graphics)

        self.dragging = False
        self.start_touch = None
        self.prev_grid_x = self.grid_x
        self.prev_grid_y = self.grid_y

    def update_pos_size(self):
        self.size = (self.grid_w * self.grid_widget.cell_size,
                     self.grid_h * self.grid_widget.cell_size)
        px, py = self.grid_widget.grid_to_pixel(self.grid_x, self.grid_y)
        self.pos = (px, py)

    def update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

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
                gx = round((self.x - self.grid_widget.x) / self.grid_widget.cell_size)
                gy = round((self.y - self.grid_widget.y) / self.grid_widget.cell_size)

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
