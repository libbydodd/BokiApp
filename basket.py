# basket.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App  # Import the App class which is the base for creating Kivy apps
from kivy.uix.label import Label  # Import the Label class to use it for displaying text
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

Builder.load_string("""
<Basket>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '10dp'
        padding: '10dp'

        Image:
            source: 'logo.png'
            size_hint_y: None
            height: '60dp'
            keep_ratio: True
            allow_stretch: True

        Label:
            text: 'Your Basket'
            font_size: '24sp'
            size_hint_y: None
            height: '50dp'

        BoxLayout:
            orientation: 'vertical'
            id: basket_items_box
            size_hint_y: None
            height: self.minimum_height

        Button:
            id: action_button
            text: 'Start Adding Items'
            size_hint_y: None
            height: '50dp'
            background_color: 1, 0, 0, 1
            on_press: root.handle_button_press()

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
        basket_items_box = self.ids.basket_items_box
        action_button = self.ids.action_button
        
        basket_items_box.clear_widgets()  # Clear the basket items container
        if not basket_items:
            action_button.text = 'Start Adding Items'
            action_button.background_color = (1, 0, 0, 1)
            action_button.on_press = lambda: setattr(self.manager, 'current', 'menu_touchpoints')
            basket_items_box.add_widget(Label(text="It looks empty here...", font_size='20sp', size_hint_y=None, height='30dp'))
        else:
            action_button.text = 'Checkout'
            action_button.background_color = (1, 0, 0, 1)
            action_button.on_press = lambda: setattr(self.manager, 'current', 'checkout_screen')  # Change to checkout screen
            for item in basket_items:
                label = Label(text=f"{item['item_name']} - £{item['price']:.2f}", size_hint_y=None, height='30dp')
                basket_items_box.add_widget(label)

    def handle_button_press(self):
        # Dynamically handling button press based on the basket content
        if not App.get_running_app().basket:
            self.manager.current = 'menu_touchpoints'
        else:
            self.manager.current = 'checkout_screen'

if __name__ == '__main__':
    from kivy.app import App

    class TestApp(App):
        def build(self):
            return Basket()

    TestApp().run()
