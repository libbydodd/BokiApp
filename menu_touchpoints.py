#menu_touchpoints.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.metrics import dp

Builder.load_string("""

<TouchpointButton@ButtonBehavior+FloatLayout>:
    source: ''
    text: ''
    size_hint_y: None
    height: Window.width / 3

    Image:
        source: root.source
        allow_stretch: True
        keep_ratio: False
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}

    FloatLayout:
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        canvas.before:
            Color:
                rgba: (0, 0, 0, 0.5)  # Tint color and opacity
            Rectangle:
                pos: self.pos
                size: self.size

    Label:
        text: root.text
        font_size: '20sp'
        color: (1, 1, 1, 1)  # White text
        size_hint: 1, 1
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        halign: 'center'
        valign: 'middle'
        text_size: self.size  # Set the text size to the size of the label

<MenuTouchpoints>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(5)

        Image:
            source: 'logo.png'
            size_hint: None, None
            size: dp(200), dp(100)
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'Where would you like to order from?'
            size_hint_y: None
            height: dp(40)
            color: 1, 1, 1, 1
            font_size: '20sp'

        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            GridLayout:
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(5)

                TouchpointButton:
                    source: 'boki_image.png'
                    text: 'Boki'
                    on_release: root.manager.current = 'collection_time'

                TouchpointButton:
                    source: 'the_hive_image.png'
                    text: 'The Hive'
                    on_release: root.manager.current = 'collection_time'

                TouchpointButton:
                    source: 'el_toro_image.png'
                    text: 'El Toro'
                    on_release: root.manager.current = 'collection_time'

        # Sticky menu
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            Button:
                text: 'Home'
                on_press: root.manager.current = 'home'
            Button:
                text: 'Menu'
            Button:
                text: 'Basket'
                on_press: root.manager.current = 'basket'
            Button:
                text: 'Account'
                on_press: root.manager.current = 'account_screen'
""")

class MenuTouchpoints(Screen):
    pass

if __name__ == '__main__':
    from kivy.app import App
    class TestApp(App):
        def build(self):
            return MenuTouchpoints()

    TestApp().run()
