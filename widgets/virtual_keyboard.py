from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button

class VirtualKeyboard(BoxLayout):
    def __init__(self, target_input, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        self.target_input = target_input

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
                btn = Button(text=char, on_press=self.insert_char)
                row_layout.add_widget(btn)
            self.add_widget(row_layout)

        # Нижний ряд: пробел, backspace, смена языка
        control_row = BoxLayout(size_hint_y=None, height=50)

        space_btn = Button(text="SPACE", on_press=lambda x: self.insert_char(" "))
        lang_btn = Button(text="SWITCH", on_press=self.switch_language)
        back_btn = Button(text="BACKSPACE", on_press=self.backspace)
        done_btn = Button(text="DONE", on_press=self.done)

        control_row.add_widget(lang_btn)
        control_row.add_widget(space_btn)
        control_row.add_widget(back_btn)
        control_row.add_widget(done_btn)

        self.add_widget(control_row)

    def insert_char(self, instance):
        char = instance if isinstance(instance, str) else instance.text
        self.target_input.text += char

    def backspace(self, instance):
        self.target_input.text = self.target_input.text[:-1]
    
    def done(self, instance):
        print("Done")

    def switch_language(self, instance):
        self.language = "RU" if self.language == "EN" else "EN"
        self.build_keyboard()