import scripts.base_button as bb
from dataclasses import dataclass
import pynput.keyboard as kb
import pynput.mouse as m
import time

@dataclass
class BlenderMirrorButton(bb.BaseButton):
    id: str = "blender_mirror"
    name: str = "Add Mirror modifier"
    category_id: str = "blender"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):

        keyboard = kb.Controller()
        mouse = m.Controller()

        mouse.position = (2120, 590)
        mouse.move(1, 0)
        mouse.move(-1, 0)

        mouse.press(m.Button.left)
        time.sleep(0.05)
        mouse.release(m.Button.left)

        time.sleep(0.1)

        mouse.position = (2253, 500)
        mouse.move(1, 0)
        mouse.move(-1, 0)

        mouse.press(m.Button.left)
        time.sleep(0.05)
        mouse.release(m.Button.left)

        time.sleep(0.1)

        keyboard.press(kb.Key.shift)
        keyboard.press('a')
        keyboard.release('a')
        keyboard.release(kb.Key.shift)

        keyboard.type('mirror')

        keyboard.press(kb.Key.enter)
        keyboard.release(kb.Key.enter)

        return super().on_press()
