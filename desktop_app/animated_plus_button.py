from kivy.uix.button import Button
from kivy.properties import ListProperty
from kivy.animation import Animation
from kivymd.uix.behaviors import HoverBehavior

class AnimatedPlusButton(Button, HoverBehavior):
    start_color = ListProperty([0.455, 0.635, 0.435, 1])
    anim_color = ListProperty([0.455, 0.635, 0.435, 1])

    def on_enter(self):
        Animation.cancel_all(self, 'anim_color')
        Animation(anim_color=[self.start_color[0] * 1.2,
                              self.start_color[1] * 1.2,
                              self.start_color[2] * 1.2,
                              self.start_color[3]], d=0.25, t='out_quad').start(self)

    def on_leave(self):
        Animation.cancel_all(self, 'anim_color')
        Animation(anim_color=self.start_color, d=0.25, t='out_quad').start(self)

    def on_press(self):
        Animation.cancel_all(self, 'anim_color')
        Animation(anim_color=[self.start_color[0] * 0.8,
                              self.start_color[1] * 0.8,
                              self.start_color[2] * 0.8,
                              self.start_color[3]], d=0.15, t='out_quad').start(self)

    def on_release(self):
        Animation.cancel_all(self, 'anim_color')
        Animation(anim_color=[self.start_color[0] * 1.1,
                              self.start_color[1] * 1.1,
                              self.start_color[2] * 1.1,
                              self.start_color[3]], d=0.2, t='out_quad').start(self)
