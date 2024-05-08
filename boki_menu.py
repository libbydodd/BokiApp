#boki_menu.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.metrics import dp
from kivy.app import App
from kivy.core.window import Window

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
            padding: [dp(10), 0]

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
                    
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            Button:
                text: 'Home'
                on_press: app.root.current = 'home'
            Button:
                text: 'Menu'
                on_press: app.root.current = 'menu_touchpoints'
            Button:
                text: 'Basket'
                on_press: app.root.current = 'basket'
            Button:
                text: 'Account'
                on_press: app.root.current = 'account_screen'  
"""

Builder.load_string(kv)

class BokiMenu(Screen):
    def on_enter(self):
        self.populate_menu_items()

    def populate_menu_items(self):
        menu_items = fetch_menu_items()
        for item in menu_items:
            category = item['category'].lower()  # Uses dictionary access
            button = Button(text=f"{item['item_name']} £{float(item['price']):.2f}", size_hint_y=None, height=dp(40))
            button.bind(on_release=lambda btn, item=item: self.show_item_popup(item))
            getattr(self.ids, f"{category}_box").add_widget(button)

    def toggle_sections(self, section):
        scroll_view = getattr(self.ids, f"{section}_box").parent
        scroll_view.height = dp(200) if scroll_view.height == 0 else 0
        scroll_view.opacity = 1 if scroll_view.height > 0 else 0
        for other_section in ['lunch', 'snacks', 'drinks']:
            if other_section != section:
                other_scroll_view = getattr(self.ids, f"{other_section}_box").parent
                other_scroll_view.height = 0
                other_scroll_view.opacity = 0

    def show_item_popup(self, item):
        popup_content = BoxLayout(orientation='vertical', padding=10, spacing=10)
        name_label = Label(text=f"Name: {item['item_name']}", size_hint_y=None, height=dp(40))
        description_label = Label(text=f"Description: {item['description']}", size_hint_y=None, text_size=(280, None), halign='left', valign='top')
        price_label = Label(text=f"Price: £{item['price']:.2f}", size_hint_y=None, height=dp(40))

        # Add to Basket Button
        add_to_basket_button = Button(
            text="Add to Basket", 
            size_hint_y=None, 
            height=dp(40),
            background_color=(1, 0, 0, 1)
        )
        add_to_basket_button.bind(on_press=lambda x: self.add_item_to_basket(item))

        popup_content.add_widget(name_label)
        popup_content.add_widget(description_label)
        popup_content.add_widget(price_label)
        popup_content.add_widget(add_to_basket_button)  # Adds the button to the popup

        # Adjusts popup height
        popup = Popup(title='Item Details', content=popup_content, size_hint=(None, None), size=(350, 400))
        popup.open()

    def add_item_to_basket(self, item):
        App.get_running_app().add_item_to_basket(item)


class BokiApp(App):
    def build(self):
        return BokiMenu()

if __name__ == '__main__':
    BokiApp().run()
