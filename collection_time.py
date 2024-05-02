from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.app import App
from kivy.metrics import dp

# Assuming logo.png is in the same directory as the script.
logo_path = 'logo.png'

kv = """
<CollectionTime>:
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(5)
        padding: [10, dp(20), 10, 10]

        BoxLayout:
            size_hint_y: None
            height: dp(50)
            Button:
                text: 'Back'
                size_hint_x: None
                width: dp(100)
                on_release: app.root.current = 'menu_touchpoints'

        Image:
            source: 'logo.png' 
            size_hint_y: None
            height: dp(60)
            keep_ratio: True
            allow_stretch: True

        Label:
            text: 'Select Collection Time'
            size_hint_y: None
            height: dp(40)
            font_size: '20sp'

        BoxLayout:
            orientation: 'vertical'

            ToggleButton:
                text: 'Morning'
                group: 'times'
                size_hint_y: None
                height: dp(50)
                on_press: root.toggle_times('morning', self.state)
            BoxLayout:
                id: morning_box
                size_hint_y: None
                height: 0  # Initially hidden
                GridLayout:
                    cols: 2
                    ToggleButton:
                        text: '08:00'
                        group: 'morning_times'
                        on_press: app.root.current = 'boki_menu'
                    ToggleButton:
                        text: '08:30'
                        group: 'morning_times'
                        on_press: app.root.current = 'boki_menu'

            ToggleButton:
                text: 'Afternoon'
                group: 'times'
                size_hint_y: None
                height: dp(50)
                on_press: root.toggle_times('afternoon', self.state)
            BoxLayout:
                id: afternoon_box
                size_hint_y: None
                height: 0  # Initially hidden
                GridLayout:
                    cols: 2
                    ToggleButton:
                        text: '12:00'
                        group: 'afternoon_times'
                        on_press: app.root.current = 'boki_menu'
                    ToggleButton:
                        text: '12:30'
                        group: 'afternoon_times'
                        on_press: app.root.current = 'boki_menu'

            ToggleButton:
                text: 'Evening'
                group: 'times'
                size_hint_y: None
                height: dp(50)
                on_press: root.toggle_times('evening', self.state)
            BoxLayout:
                id: evening_box
                size_hint_y: None
                height: 0  # Initially hidden
                GridLayout:
                    cols: 2
                    ToggleButton:
                        text: '17:00'
                        group: 'evening_times'
                        on_press: app.root.current = 'boki_menu'
                    ToggleButton:
                        text: '17:30'
                        group: 'evening_times'
                        on_press: app.root.current = 'boki_menu'

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

class CollectionTime(Screen):
    def toggle_times(self, period, state):
        box_id = period.lower() + '_box'
        box = self.ids[box_id]
        if state == 'down':
            # Show the times
            box.height = dp(200)  # Adjust this based on the number of buttons
            box.opacity = 1
        else:
            # Hide the times
            box.height = 0
            box.opacity = 0
        # Ensure all other boxes are closed
        for other_period, other_box_id in {'morning': 'morning_box', 'afternoon': 'afternoon_box', 'evening': 'evening_box'}.items():
            if other_period != period:
                other_box = self.ids[other_box_id]
                other_box.height = 0
                other_box.opacity = 0

class CollectionApp(App):
    def build(self):
        return CollectionTime()

if __name__ == '__main__':
    CollectionApp().run()
