# basket.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App  # Import the App class which is the base for creating Kivy apps
from kivy.uix.label import Label  # Import the Label class to use it for displaying text

Builder.load_string("""
<Basket>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'
        id: basket_box  # Ensure there's an ID for dynamic content

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
    def on_pre_enter(self):
        basket_items = App.get_running_app().basket
        self.ids.basket_box.clear_widgets()
        if not basket_items:
            self.ids.basket_box.add_widget(Label(text="It looks empty here...", font_size='20sp', size_hint_y=None, height='30dp'))
        else:
            for item in basket_items:
                label = Label(text=f"{item['name']} - £{item['price']:.2f}", size_hint_y=None, height='30dp')
                self.ids.basket_box.add_widget(label)