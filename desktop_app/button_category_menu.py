from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty, BooleanProperty, StringProperty, ObjectProperty, DictProperty
from kivy.clock import Clock
from kivy.app import App
from button_types_util import buttonTypesUtilInstance
from deck_area import DeckArea

class ButtonTypeItem(Button):
    '''Виджет кнопки внутри категории'''
    type_name = StringProperty('')
    
    button_id = StringProperty('')
    button_category_id = StringProperty('')

    def on_press(self):
        super().on_press()
        App.get_running_app().layout.overlay_menu.dismiss()
        button_info = buttonTypesUtilInstance.get_button_info(self.button_category_id, self.button_id)
        deck_area:DeckArea = App.get_running_app().get_deck_area()
        free_spot = deck_area.find_first_free_spot(button_info["size_x"], button_info["size_y"])
        if not free_spot:
            print("No button place found")
            return
        deck_area.add_deck_button(
            emoji=button_info['emoji'], image_source=button_info['icon'],
            hue=button_info['color'], 
            grid_x=free_spot[0], grid_y=free_spot[1], 
            grid_w=button_info["size_x"], grid_h=button_info["size_y"]
        )

class ButtonCategoryItem(BoxLayout):
    '''Категория кнопок, раскрывающаяся по нажатию'''
    category_name = StringProperty('')
    category_id = StringProperty('')
    expanded = BooleanProperty(False)
    button_types = DictProperty({})

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
            for btn_type in self.button_types.items():
                self.types_box.add_widget(
                    ButtonTypeItem(
                        button_id=btn_type[0],               # id
                        type_name=btn_type[1],               # display_name
                        button_category_id=self.category_id, # category_id
                        size_hint_y=None, 
                        height=48)
                    )
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
            box.add_widget(ButtonCategoryItem(
                category_id=cat['id'],
                category_name=cat['name'], 
                button_types=cat['types'],
                )
            )
        scroll.add_widget(box)
        self.add_widget(scroll)
