import os
import json

class ButtonTypesUtil:
    def __init__(self, json_path=None):
        if json_path is None:
            json_path = os.path.join(os.path.dirname(__file__), 'button_types.json')
        self.json_path = json_path
        self._data = None

    def _load(self):
        if self._data is None:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)

    def get_categories(self):
        """
        Возвращает список категорий с display_name для каждой кнопки.
        [{ 'id' ..., 'name': ..., 'types': {id:display_name, ...} }]
        """
        self._load()
        categories = []
        for cat in self._data:
            categories.append({
                'id': cat['category_id'],
                'name': cat['category_display_name'],
                'types': dict(zip(
                    [btn.get('id')for btn in cat.get('buttons', [])],
                    [btn.get('display_name') or btn.get('emoji') or btn.get('icon') or btn.get('script') or ''
                    for btn in cat.get('buttons', [])]
                ))
            })
        return categories

    def get_button_info(self, category_id, button_id):
        """
        Возвращает dict с полной информацией о кнопке по имени категории и id кнопки.
        Если не найдено — возвращает None.
        """
        self._load()
        for cat in self._data:
            if cat['category_id'] == category_id:
                for btn in cat.get('buttons', []):
                    if btn.get('id') == button_id:
                        return btn
        return None

buttonTypesUtilInstance = ButtonTypesUtil()