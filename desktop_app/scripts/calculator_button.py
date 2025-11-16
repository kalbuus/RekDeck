import scripts.base_button as bb
from dataclasses import dataclass

@dataclass
class CalculatorButton(bb.BaseButton):
    id: str = "calculator_button"
    name: str = "Calculator"
    icon: str = None
    def __init__(self, **kwargs):
        super().__init__()

    def on_press(self):
        pass
        return super().on_press()
