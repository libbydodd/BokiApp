# login_screen.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '15dp'
        padding: '50dp', '120dp', '50dp', '120dp'
        canvas.before:
            Color:
                rgba: (28/255, 25/255, 25/255, 1)  # Dark background color
            Rectangle:
                pos: self.pos
                size: self.size

        Image:
            source: 'logo.png'
            size_hint: None, None
            size: '200dp', '200dp'
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'Login'
            color: 1, 1, 1, 1
            size_hint_y: None
            height: '48dp'
            font_size: '24sp'

        TextInput:
            id: username_input
            hint_text: 'Username'
            size_hint_y: None
            height: '48dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
            padding: '10dp'

        TextInput:
            id: password_input
            hint_text: 'Password'
            size_hint_y: None
            height: '48dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
            padding: '10dp'
            password: True

        Button:
            text: 'Login'
            size_hint_y: None
            height: '48dp'
            background_color: 1, 0, 0, 1  # Red color for the button
            on_press: root.login()

        Label:
            text: 'or'
            size_hint_y: None
            height: '20dp'
            color: 1, 1, 1, 1

        Button:
            text: 'Register'
            size_hint_y: None
            height: '48dp'
            background_normal: ''
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            on_press: root.manager.current = 'register_screen'
""")

class LoginScreen(Screen):
    def login(self):
        # Placeholder for login logic
        # Here, you should verify the user's credentials
        print(f"Logging in with {self.ids.username_input.text}")
        # Assuming the credentials are correct, transition to the home screen
        self.manager.current = 'home'
