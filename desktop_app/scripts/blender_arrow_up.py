import scripts.base_button as bb
from dataclasses import dataclass
from pynput.keyboard import Key, Controller

@dataclass
class BlenderCamButton(bb.BaseButton):
    id: str = "blender_move_up"
    name: str = "Move up"
    category_id: str = "blender"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):
        keyboard = Controller()

        keyboard.type('gz1')

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        return super().on_press()
