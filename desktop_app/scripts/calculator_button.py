import scripts.base_button as bb
from dataclasses import dataclass
import os

@dataclass
class CalculatorButton(bb.BaseButton):
    id: str = "calculator_button"
    name: str = "Open Calculator"
    category_id: str = "apps"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):
        os.system('calc')
        return super().on_press()
