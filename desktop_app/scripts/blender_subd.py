import scripts.base_button as bb
from dataclasses import dataclass
from pynput.keyboard import Key, Controller
import time

@dataclass
class BlenderSubdButton(bb.BaseButton):
    id: str = "blender_subd"
    name: str = "Add Subdivision Surface"
    category_id: str = "blender"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):

        keyboard = Controller()
        
        keyboard.press(Key.ctrl)
        keyboard.press('1')
        keyboard.release('1')
        keyboard.release(Key.ctrl)

        return super().on_press()
