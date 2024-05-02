# basket.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<Basket>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'

        Label:
            text: 'Your Basket'
            font_size: '24sp'
            size_hint_y: None
            height: '50dp'

        Label:
            text: 'It looks empty here...'
            font_size: '20sp'
            size_hint_y: None
            height: '30dp'

        Button:
            text: 'Start Adding Items'
            size_hint_y: None
            height: '50dp'
            on_press: root.manager.current = 'menu_touchpoints'

        # Sticky menu at the bottom
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            Button:
                text: 'Home'
                on_press: root.manager.current = 'home'
            Button:
                text: 'Menu'
                on_press: root.manager.current = 'menu_touchpoints'
            Button:
                text: 'Basket'
            Button:
                text: 'Account'
                on_press: root.manager.current = 'account_screen'
""")

class Basket(Screen):
    pass
