from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty, BooleanProperty, StringProperty, ObjectProperty, DictProperty
from kivy.clock import Clock
from kivy.app import App
from deck_area import DeckArea

class ButtonTypeItem(Button):
    '''Виджет кнопки внутри категории'''
    type_name = StringProperty('')
    
    button_id = StringProperty('')
    button_category_id = StringProperty('')

    def on_press(self):
        super().on_press()
        layout = App.get_running_app().layout
        layout.overlay_menu.dismiss()
        layout.show_settings_menu(self.button_id)
        settings_menu = layout.button_settings_menu

        x_size_index = settings_menu.create_labeled_slider(
            Label(text="Размер по X", size_hint_x=None),
            Slider(min=1, max=5, step=1, value_track=True, value_track_color=[0.3, 0.3, 0.6, 1]),
            Label(text="1", size_hint_x=0.15),
            "size_x"
        )
        x_size_slider = settings_menu.one_line_settings[settings_menu.settings[x_size_index]][1]
        y_size_index = settings_menu.create_labeled_slider(
            Label(text="Размер по Y", size_hint_x=None),
            Slider(min=1, max=3, step=1, value_track=True, value_track_color=[0.3, 0.3, 0.6, 1]),
            Label(text="1", size_hint_x=0.15),
            "size_y"
        )
        y_size_slider = settings_menu.one_line_settings[settings_menu.settings[y_size_index]][1]
        color_index = settings_menu.add_one_line_settings([
            Label(text="Цвет", size_hint_x=None),
            Slider(min=0, max=1)],
            1,
            "color"
        )
        color_slider = settings_menu.one_line_settings[settings_menu.settings[color_index]][1]

        # Иконка
        import tkinter as tk
        from tkinter import filedialog
        import os

        class IconSelectWidget(BoxLayout):
            def __init__(self, **kwargs):
                super().__init__(orientation='horizontal', spacing=8, size_hint_y=None, height=32, **kwargs)
                self.label = Label(text="Иконка", size_hint_x=0.5)
                self.button = Button(text="Выбрать файл", size_hint_x=0.5)
                self.button.bind(on_release=self.open_file_dialog)
                self.add_widget(self.label)
                self.add_widget(self.button)
                self.selected_path = None

            def open_file_dialog(self, *args):
                # Открываем стандартный диалог выбора файла через tkinter
                root = tk.Tk()
                root.withdraw()
                file_path = filedialog.askopenfilename(
                    title="Выберите иконку",
                    initialdir=os.path.dirname(os.path.abspath(__file__)+ r"\assets"),
                    filetypes=[("Изображения", "*.png;*.jpg;*.jpeg;*.ico;*.bmp;*.gif"), ("Все файлы", "*.*")]
                )
                root.destroy()
                if file_path:
                    self.selected_path = file_path
                    self.button.text = "Выбрано"
                else:
                    self.button.text = "Выбрать файл"

        icon_widget = IconSelectWidget()
        settings_menu.add_one_line_settings([icon_widget], 0, "icon")

        def on_value_changed(instance, value):
            layout = App.get_running_app().layout
            layout.button_settings_menu.create_button_visualisation(x_size_slider.value, y_size_slider.value, color_slider.value)
        x_size_slider.bind(value=on_value_changed)
        y_size_slider.bind(value=on_value_changed)
        color_slider.bind(value=on_value_changed)
    


class ButtonCategoryItem(BoxLayout):
    '''Категория кнопок, раскрывающаяся по нажатию'''
    category_name = StringProperty('')
    category_id = StringProperty('')
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
            for script in self.button_types:
                self.types_box.add_widget(
                    ButtonTypeItem(
                        button_id=script.id,                 # id
                        type_name=script.name,               # display_name
                        button_category_id=self.category_id, # category_id
                        size_hint_y=None, 
                        height=48)
                    )
            self.height = 48 + self.types_box.height
        else:
            self.types_box.height = 0
            self.height = 48

class ButtonCategoryMenu(ModalView):
    '''Меню выбора категории кнопок'''
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
                button_types=cat['buttons'],
                )
            )
        scroll.add_widget(box)
        self.add_widget(scroll)
