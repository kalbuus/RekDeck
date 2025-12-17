import scripts.base_button as bb
from dataclasses import dataclass
import os

@dataclass
class BlenderButton(bb.BaseButton):
    id: str = "blender_button"
    name: str = "Open Blender"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):
        os.startfile(r'C:\Program Files (x86)\Steam\steamapps\common\Blender\blender.exe')
        return super().on_press()
