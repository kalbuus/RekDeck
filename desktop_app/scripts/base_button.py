from dataclasses import dataclass

@dataclass
class BaseButton:
    id: str = "base_button"
    name: str = "No name"
    icon: str = None

    min_width: int = 1
    min_height: int = 1

    max_width: int = None
    max_height: int = None

    category_id: str = "undefined"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            # проверяем, есть ли такой атрибут в классе
            if hasattr(self, key):
                # применяем атрибут
                setattr(self, key, value)
            else:
                raise AttributeError(f"Unknown parameter '{key}' for {self.__class__.__name__}")

    def on_press(self):
        pass

    def on_drag(self):
        pass

    def on_release(self):
        pass

    def on_draw(self, surface):
        pass

    def on_tick(self, dt):
        pass

    def send_all_parameters(self):
        pass

    def send_selected_parameters(self, params):
        pass

    def load_kv(self):
        pass
