# register_screen.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
import mysql.connector
import hashlib
from kivy.core.window import Window

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
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        email = self.ids.email.text
        password = self.ids.password.text
        confirm_password = self.ids.confirm_password.text
        
        if password != confirm_password:
            print("Passwords do not match")
            return
        
        username = self.generate_unique_username(first_name, last_name)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user_id = self.register_user(username, hashed_password, email)
        if user_id:
            print(f"Account created successfully. Username: {username}")
            App.get_running_app().set_current_user(user_id)
            self.manager.current = 'dietary_requirements_screen'
        else:
            print("Failed to create account. Please try again.")

    def generate_unique_username(self, first_name, last_name):
        base_username = f"{first_name.lower()}{last_name.lower()}"
        unique_username = base_username
        num_suffix = 1
        connection = mysql.connector.connect(host='localhost', user='root', password='Harryfreddie99!', database='menu_database')
        cursor = connection.cursor()
        while True:
            cursor.execute("SELECT EXISTS(SELECT 1 FROM users WHERE username = %s)", (unique_username,))
            if cursor.fetchone()[0]:
                unique_username = f"{base_username}{num_suffix}"
                num_suffix += 1
            else:
                break
        cursor.close()
        connection.close()
        return unique_username

    def register_user(self, username, password, email):
        connection = mysql.connector.connect(host='localhost', user='root', password='Harryfreddie99!', database='menu_database')
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
            connection.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            user_id = cursor.fetchone()[0]
            return user_id
        except mysql.connector.Error as error:
            print(f"Failed to insert record: {error}")
            return None
        finally:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    from kivy.app import App
    class TestApp(App):
        def build(self):
            return RegisterScreen()

    TestApp().run()
