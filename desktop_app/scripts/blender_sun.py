import scripts.base_button as bb
from dataclasses import dataclass
from pynput.keyboard import Key, Controller

@dataclass
class BlenderSunButton(bb.BaseButton):
    id: str = "blender_sun"
    name: str = "Spawn Sun"
    category_id: str = "blender"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):
        keyboard = Controller()

        keyboard.press(Key.shift)
        keyboard.press('a')
        keyboard.release('a')
        keyboard.release(Key.shift)

        keyboard.type('sun')

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        return super().on_press()
