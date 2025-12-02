from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, ObjectProperty, DictProperty, StringProperty
from kivy.lang import Builder
from kivy.app import App

from grid_widget import GridWidget
from deck_button import DeckButton
from deck_area import DeckArea

class ButtonSettingsMenu(ModalView):
    settings = ListProperty([])  # Список виджетов настроек
    one_line_settings = DictProperty({})
    content_box = ObjectProperty(None)
    grid = ObjectProperty(None)
    btn = ObjectProperty(None)

    props = DictProperty({})

    button_id = StringProperty()

    def __init__(self, button_id, **kwargs):
        super().__init__(**kwargs)
        self.bind(settings=self._update_settings)
        self.button_id = button_id
        self.create_button_visualisation(1, 1, 0, "")

    def on_open(self):
        self.content_box = self.ids.content_box
        self._update_settings()
        return super().on_open()
    
    def preset_settings(self, button_id, w, h, color, icon):
        self.create_button_visualisation(w, h, color, icon)
        self.button_id = button_id

    def create_labeled_slider(self, label1, slider, label2, settings_id):
        bl_index = self.add_one_line_settings([
            label1,
            slider,
            label2],
            1,
            settings_id)
        
        def OnValueChange(instance,value):
            layout = App.get_running_app().layout
            dyn_label_grid_x = layout.button_settings_menu.one_line_settings[instance.parent][2]
            dyn_label_grid_x.text = str(value)
        self.one_line_settings[self.settings[bl_index]][1].bind(value=OnValueChange)

        return bl_index
    
    def add_one_line_settings(self, widgets, setting_index = None, settings_id = None):
        bl_index = self.add_setting(BoxLayout(orientation="horizontal"))
        bl = self.settings[bl_index]
        for widget in range(len(widgets)):
            bl.add_widget(widgets[widget])

            if setting_index == widget and settings_id:
                self.props[settings_id] = widgets[widget]

            if bl not in self.one_line_settings:
                self.one_line_settings[bl] = [widgets[widget]]
            else:
                self.one_line_settings[bl].append(widgets[widget])
        return bl_index

    def add_setting(self, setting_widget, settings_id = None):
        self.settings.append(setting_widget)
        if settings_id:
            self.props[settings_id] = setting_widget
        return len(self.settings) - 1 # Возвращаем положение нового виджета

    def on_apply(self):
        self.dismiss()

        deck_area:DeckArea = App.get_running_app().get_deck_area()
        free_spot = deck_area.find_first_free_spot(self.props["size_x"].value, self.props["size_y"].value)
        if not free_spot:
            print("No button place found")
            return
        deck_area.add_deck_button(
            image_source=self.props['icon'].selected_path,
            hue=self.props['color'].value, 
            grid_x=free_spot[0], grid_y=free_spot[1], 
            grid_w=self.props["size_x"].value, grid_h=self.props["size_y"].value,
            button_id=self.button_id
        )

        pass

    def create_button_visualisation(self, w, h, color, icon):
        if self.grid:
            self.ids.float_grid_layout.remove_widget(self.grid)
        if self.btn:
            self.ids.float_grid_layout.remove_widget(self.btn)

        self.grid = GridWidget(cols=w, rows=h, size_hint=(1, 1), pos_hint={"center_x": 0.5, "center_y": 0.5})
        self.ids.float_grid_layout.add_widget(self.grid)
        self.btn = DeckButton(
            grid_widget=self.grid, 
            image_source=icon, 
            can_move=False, grid_w=w, grid_h=h, hue=color)
        self.ids.float_grid_layout.add_widget(self.btn)

    def clear_settings(self):
        self.settings = []

    def _update_settings(self, *args):
        if self.content_box:
            self.content_box.clear_widgets()
            for widget in self.settings:
                self.content_box.add_widget(widget)
