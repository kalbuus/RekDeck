import scripts.base_button as bb
from dataclasses import dataclass
import pynput.keyboard as kb
import pynput.mouse as m
import time

@dataclass
class BlenderMaterialButton(bb.BaseButton):
    id: str = "blender_material"
    name: str = "Add Material"
    category_id: str = "blender"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):
        
        mouse = m.Controller()

        mouse.position = (2121, 730)
        mouse.move(1, 0)
        mouse.move(-1, 0)

        mouse.press(m.Button.left)
        time.sleep(0.05)
        mouse.release(m.Button.left)

        time.sleep(0.3)

        mouse.position = (2360, 460)
        mouse.move(1, 0)
        mouse.move(-1, 0)

        mouse.press(m.Button.left)
        time.sleep(0.05)
        mouse.release(m.Button.left)

        return super().on_press()
