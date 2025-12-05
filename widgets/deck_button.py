from kivy.uix.widget import Widget
from kivy.core.text import Label as CoreLabel
from kivy.properties import NumericProperty, BooleanProperty, ObjectProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.app import App

class DeckButton(Widget):
    def on_hue(self, instance, value):
        self.anim_color = self.get_hsv_color()

    image_source = ObjectProperty(None)
    hue = NumericProperty(0.1)
    selected = BooleanProperty(False)
    anim_color = ObjectProperty([0.1, 0.6, 0.9, 1])
    icon_fit_button = BooleanProperty(False)

    button_id = StringProperty(None)

    grid_x = NumericProperty(0)
    grid_y = NumericProperty(0)
    grid_w = NumericProperty(1)
    grid_h = NumericProperty(1)
    grid_widget = ObjectProperty(None)

    def get_hsv_color(self, selected=None):
        import colorsys
        h = getattr(self, 'hue', 0.1)
        s = 0.4
        if selected is None:
            selected = self.selected
        v = 0.5 if selected else 0.8
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return [r, g, b, 1]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.anim_color = self.get_hsv_color()

        self.prev_grid_x = self.grid_x
        self.prev_grid_y = self.grid_y

        if self.grid_widget:
            self._bind_to_grid_widget(self.grid_widget)
            self.update_pos_size()

    def _bind_to_grid_widget(self, grid_widget):
        if hasattr(self, '_grid_widget_binds'):
            for prop, uid in self._grid_widget_binds:
                grid_widget.unbind_uid(prop, uid)
        self._grid_widget_binds = []
        if grid_widget:
            for prop in ('width', 'height', 'cols', 'rows', 'pos', 'center_x', 'center_y'):
                uid = grid_widget.fbind(prop, self.update_pos_size)
                self._grid_widget_binds.append((prop, uid))

    def update_pos_size(self, *args):
        if not self.grid_widget or getattr(self.grid_widget, 'cols', 0) == 0:
            return
        cell_size = self.grid_widget.width / self.grid_widget.cols
        self.size = (self.grid_w * cell_size, self.grid_h * cell_size)
        try:
            px, py = self.grid_widget.grid_to_pixel(self.grid_x, self.grid_y)
            self.pos = (px, py)
        except Exception:
            pass

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
            try:
                Animation.cancel_all(self, 'anim_color')
                Animation(anim_color=self.get_hsv_color(True), d=0.08, t='out_quad').start(self)
                
            except Exception:
                pass
            return True
        return super().on_touch_down(touch)
    
    def on_touch_up(self, touch):
        try:
            Animation.cancel_all(self, 'anim_color')
            Animation(anim_color=self.get_hsv_color(False), d=0.2, t='out_quad').start(self)
        except Exception:
            pass
        return super().on_touch_up(touch)

