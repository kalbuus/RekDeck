from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty, BooleanProperty, StringProperty, ObjectProperty
from kivy.clock import Clock
from kivy.app import App

class ButtonTypeItem(Button):
    '''Виджет кнопки внутри категории'''
    type_name = StringProperty('')

    def on_press(self):
        super().on_press()
        App.get_running_app().layout.overlay_menu.dismiss()
    # Здесь можно добавить визуализацию типа кнопки

class ButtonCategoryItem(BoxLayout):
    '''Категория кнопок, раскрывающаяся по нажатию'''
    category_name = StringProperty('')
    expanded = BooleanProperty(False)
    button_types = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.update_types(), 0)

    def toggle(self, *args):
        self.expanded = not self.expanded
        self.update_types()


    def update_types(self):
        self.types_box.clear_widgets()
        if self.expanded:
            self.types_box.height = len(self.button_types) * 48
            for btn_type in self.button_types:
                self.types_box.add_widget(ButtonTypeItem(type_name=btn_type, size_hint_y=None, height=48))
            self.height = 48 + self.types_box.height
        else:
            self.types_box.height = 0
            self.height = 48

class ButtonCategoryMenu(ModalView):
    '''Меню выбора категории кнопок с затемнением фона'''
    categories = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll = ScrollView(size_hint=(None, None), 
                            size=(600, 500), 
                            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        box = BoxLayout(orientation='vertical', size_hint_y=None)
        box.bind(minimum_height=box.setter('height'))
        for cat in self.categories:
            box.add_widget(ButtonCategoryItem(category_name=cat['name'], button_types=cat['types']))
        scroll.add_widget(box)
        self.add_widget(scroll)
