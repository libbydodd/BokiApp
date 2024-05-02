# register_screen.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

kv = """
<RegisterScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '15dp'
        padding: '50dp', '100dp', '50dp', '50dp'
        Image:
            source: 'logo.png'
            size_hint: None, None
            size: '200dp', '200dp'
            pos_hint: {'center_x': 0.5}
        Label:
            text: "Register"
            font_size: '24sp'
            color: 1, 1, 1, 1
            size_hint_y: None
            height: '48dp'
        TextInput:
            id: first_name
            hint_text: "First name"
            multiline: False
            size_hint_y: None
            height: '48dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
        TextInput:
            id: last_name
            hint_text: "Last name"
            multiline: False
            size_hint_y: None
            height: '48dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
        TextInput:
            id: email
            hint_text: "Email"
            multiline: False
            size_hint_y: None
            height: '48dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
        TextInput:
            id: password
            hint_text: "Enter password"
            password: True
            multiline: False
            size_hint_y: None
            height: '48dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
        TextInput:
            id: confirm_password
            hint_text: "Confirm password"
            password: True
            multiline: False
            size_hint_y: None
            height: '48dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
        Button:
            text: "Create account"
            size_hint_y: None
            height: '48dp'
            background_color: 0.65, 0.08, 0.08, 1
            on_release: root.create_account()
        Button:
            text: "Back to login"
            size_hint_y: None
            height: '48dp'
            background_normal: ''
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            on_release: root.manager.current = 'login_screen'
"""

Builder.load_string(kv)

class RegisterScreen(Screen):
    def create_account(self):
        # Here you would add logic for creating an account, e.g., checking passwords,
        # saving user data, handling errors, etc.
        # For now, it simply switches to the dietary requirements screen
        self.manager.current = 'dietary_requirements_screen'
