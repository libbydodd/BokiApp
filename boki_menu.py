from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.app import App

# Importing the function to fetch menu items from the database
from db import fetch_menu_items

# Kivy layout definition using Builder
kv = """
<BokiMenu>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10, 10, 10, 10
        spacing: 10

        BoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: [dp(10), 0]  # Add padding around the button

            Button:
                text: 'Back'
                size_hint: None, None
                width: dp(100)
                height: dp(40)
                pos_hint: {'center_y': 0.5}
                on_press: app.root.current = 'collection_time'

        Image:
            source: 'logo.png'
            size_hint_y: None
            height: dp(60)
            keep_ratio: True
            allow_stretch: True

        Label:
            text: 'Boki Menu'
            size_hint_y: None
            height: dp(40)
            font_size: '24sp'

        BoxLayout:
            orientation: 'vertical'

            ToggleButton:
                text: 'Lunch'
                group: 'menu'
                size_hint_y: None
                height: dp(50)
                on_press: root.toggle_sections('lunch')
            ScrollView:
                size_hint_y: None
                height: 0
                BoxLayout:
                    id: lunch_box
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height

            ToggleButton:
                text: 'Snacks'
                group: 'menu'
                size_hint_y: None
                height: dp(50)
                on_press: root.toggle_sections('snacks')
            ScrollView:
                size_hint_y: None
                height: 0
                BoxLayout:
                    id: snacks_box
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height

            ToggleButton:
                text: 'Drinks'
                group: 'menu'
                size_hint_y: None
                height: dp(50)
                on_press: root.toggle_sections('drinks')
            ScrollView:
                size_hint_y: None
                height: 0
                BoxLayout:
                    id: drinks_box
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
"""

Builder.load_string(kv)

class BokiMenu(Screen):
    def on_enter(self):
        self.populate_menu_items()

    def populate_menu_items(self):
        menu_items = fetch_menu_items()
        for item in menu_items:
            category = item[4].lower()
            button = Button(text=f"{item[1]} £{float(item[3]):.2f}", size_hint_y=None, height=dp(40))
            if category == 'lunch':
                self.ids.lunch_box.add_widget(button)
            elif category == 'snacks':
                self.ids.snacks_box.add_widget(button)
            elif category == 'drinks':
                self.ids.drinks_box.add_widget(button)

    def toggle_sections(self, section):
        scroll_view = self.ids.get(f"{section}_box").parent
        if scroll_view:
            scroll_view.height = dp(200) if scroll_view.height == 0 else 0
            scroll_view.opacity = 1 if scroll_view.height > 0 else 0

            for other_section in ['lunch', 'snacks', 'drinks']:
                if other_section != section:
                    other_scroll_view = self.ids.get(f"{other_section}_box").parent
                    if other_scroll_view:
                        other_scroll_view.height = 0
                        other_scroll_view.opacity = 0

class BokiApp(App):
    def build(self):
        return BokiMenu()

if __name__ == '__main__':
    BokiApp().run()
