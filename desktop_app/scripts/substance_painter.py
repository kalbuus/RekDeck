import scripts.base_button as bb
from dataclasses import dataclass
import os

@dataclass
class BlenderButton(bb.BaseButton):
    id: str = "substance_painter_button"
    name: str = "Open Substance Painter"
    category_id: str = "apps"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):
        os.startfile(r'C:\Program Files\Adobe\Adobe Substance 3D Painter\Adobe Substance 3D Painter.exe')
        return super().on_press()
