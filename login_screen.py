# login_screen.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
import mysql.connector
import hashlib

Builder.load_string("""
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '15dp'
        padding: '50dp', '120dp', '50dp', '120dp'
        canvas.before:
            Color:
                rgba: (28/255, 25/255, 25/255, 1)
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
            font_size: '24sp'
            size_hint_y: None
            height: '48dp'
            color: 1, 1, 1, 1
        TextInput:
            id: username_input
            hint_text: 'Username'
            size_hint_y: None
            height: '48dp'
            padding: '10dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
        TextInput:
            id: password_input
            hint_text: 'Password'
            password: True
            size_hint_y: None
            height: '48dp'
            padding: '10dp'
            foreground_color: 1, 1, 1, 1
            background_color: 0, 0, 0, 0
        Button:
            text: 'Login'
            size_hint_y: None
            height: '48dp'
            background_color: 1, 0, 0, 1
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
            background_color: 1, 1, 1, 1
            color: 0, 0, 0, 1
            on_press: root.manager.current = 'register_screen'
""")

class LoginScreen(Screen):
    def login(self):
        username = self.ids.username_input.text
        password = self.ids.password_input.text
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        connection = mysql.connector.connect(host='localhost', user='root', password='Harryfreddie99!', database='menu_database')
        cursor = connection.cursor()
        try:
            cursor.execute("SELECT user_id FROM users WHERE username = %s AND password = %s", (username, hashed_password))
            user_id = cursor.fetchone()
            if user_id:
                App.get_running_app().set_current_user(user_id[0])
                self.manager.current = 'home'
            else:
                print("Invalid username or password.")
        finally:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    from kivy.app import App
    class TestApp(App):
        def build(self):
            return LoginScreen()

    TestApp().run()
