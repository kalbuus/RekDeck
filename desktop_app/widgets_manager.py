import importlib
import pkgutil
import scripts
import json

class WidgetsManager:
    def load_button_categories(self, file_path="categories.json"):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                self.categories = json.load(f)
        except FileNotFoundError:
            print(f"Error: Категории кнопок не загружены: {file_path}")
            return
        except json.JSONDecodeError:
            print(f"Error: Неправильный json формат файла категорий: {file_path}")
            return

    def load_button_classes(self):
        button_classes = {}
        package = scripts
        for _, module_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f"{package.__name__}.{module_name}")
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type) and hasattr(attr, "on_press"):
                    button_classes[attr.id] = attr()
        print(f"Загружено {len(button_classes)} виджетов!")
        return button_classes
    
    def get_categories(self):
        parsed_categories = []

        for cat in self.categories:
            parsed_categories.append({
                "id": cat, 
                "name": self.categories[cat], 
                "buttons": [self.all_buttons[b] for b in self.all_buttons if self.all_buttons[b].category_id == cat]
            })

        return parsed_categories
    
    def get_button_by_id(self, button_id):
        return self.all_buttons[button_id]

    def __init__(self):
        self.all_buttons = self.load_button_classes()
        self.load_button_categories()
