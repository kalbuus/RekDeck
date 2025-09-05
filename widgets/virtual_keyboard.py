from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class VirtualKeyboard(BoxLayout):
    def __init__(self, target_input, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.target_input = target_input

        self.shift_enabled = False
        self.language = "EN"

        self.layouts = {
            "EN": [
                list("`~1234567890-_+="),
                list("qwertyuiop"),
                list("asdfghjkl"),
                list("zxcvbnm"),
            ],
            "RU": [
                list("ё1234567890-_+="),
                list("йцукенгшщзх"),
                list("фывапролджэ"),
                list("ячсмитьбю"),
            ]
        }

        self.build_keyboard()

    def build_keyboard(self):
        self.clear_widgets()

        for row in self.layouts[self.language]:
            row_layout = GridLayout(cols=len(row))
            for char in row:
                btn = KeyboardButton(text=self.apply_shift(char), on_press=self.insert_char)
                row_layout.add_widget(btn)
            self.add_widget(row_layout)

        # Нижний ряд: пробел, backspace, смена языка
        control_row = BoxLayout(size_hint_y=None, height=50)

        shift_btn = KeyboardButton(text="SHIFT", on_press=self.toggle_shift, size_hint=(0.5, 1))
        lang_btn = KeyboardButton(text="LANG", on_press=self.switch_language, size_hint=(0.3, 1))
        space_btn = KeyboardButton(text=" ", on_press=lambda x: self.insert_char(" "), size_hint=(1, 1))
        back_btn = KeyboardButton(text="BACKSPACE", on_press=self.backspace, size_hint=(0.6, 1))
        done_btn = KeyboardButton(text="DONE", on_press=self.done, size_hint=(0.5, 1))

        control_row.add_widget(shift_btn)
        control_row.add_widget(lang_btn)
        control_row.add_widget(space_btn)
        control_row.add_widget(back_btn)
        control_row.add_widget(done_btn)

        self.add_widget(control_row)

    def insert_char(self, instance):
        char = instance if isinstance(instance, str) else instance.text
        self.target_input.text += char

        if self.shift_enabled and not isinstance(instance, str):
            self.shift_enabled = False
            self.build_keyboard()

    def backspace(self, instance):
        self.target_input.text = self.target_input.text[:-1]
    
    def apply_shift(self, char):
        return char.upper() if self.shift_enabled else char.lower()
    
    def done(self, instance):
        print("Done")
    
    def toggle_shift(self, instance):
        self.shift_enabled = not self.shift_enabled
        self.build_keyboard()

    def switch_language(self, instance):
        self.language = "RU" if self.language == "EN" else "EN"
        self.build_keyboard()


class KeyboardButton(Button):
    pass