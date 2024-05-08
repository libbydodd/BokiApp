import unittest
import hashlib
import uuid
from Main import MyApp
from kivy.core.window import Window
from db import create_connection, fetch_menu_items
import time
import mysql.connector

class TestBokiApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = MyApp()
        cls.app.build()
        cls.app.sm.current = 'login_screen'
        cls.login_screen = cls.app.sm.get_screen('login_screen')
        cls.register_screen = cls.app.sm.get_screen('register_screen')
        cls.dietary_screen = cls.app.sm.get_screen('dietary_requirements_screen')
        cls.preferences_screen = cls.app.sm.get_screen('preferences_screen')

    def test_create_connection(self):
        connection = create_connection()
        self.assertIsNotNone(connection, "Failed to create database connection")
        if connection:
            connection.close()

    def test_fetch_menu_items(self):
        items = fetch_menu_items()
        self.assertIsInstance(items, list, "Menu items should be returned as a list")

    def test_login(self):
        username = f'test_user_{uuid.uuid4().hex[:8]}'  # Ensure unique username
        password = 'password123'
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        connection = create_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                           (username, hashed_password, f'{username}@example.com'))
            connection.commit()
        except mysql.connector.errors.IntegrityError as e:
            self.fail(f"Integrity error: {e}")
        finally:
            cursor.close()
            connection.close()

        self.login_screen.ids.username_input.text = username
        self.login_screen.ids.password_input.text = password
        self.login_screen.login()
        self.assertIsNotNone(self.app.current_user_id, "Login failed with correct credentials")

    def test_register_user(self):
        first_name = "John"
        last_name = "Doe"
        email = f"john.doe_{uuid.uuid4().hex[:8]}@example.com"  # Ensure unique email
        username = f'test_user_{uuid.uuid4().hex[:8]}'  # Ensure unique username
        password = "password123"

        self.register_screen.ids.first_name.text = first_name
        self.register_screen.ids.last_name.text = last_name
        self.register_screen.ids.email.text = email
        self.register_screen.ids.username.text = username
        self.register_screen.ids.password.text = password
        self.register_screen.ids.confirm_password.text = password
        self.register_screen.create_account()

        retries = 3
        while retries > 0:
            try:
                self.assertIsNotNone(self.app.current_user_id, "Registration failed")
                break
            except AssertionError:
                retries -= 1
                if retries == 0:
                    self.fail("Registration failed after multiple retries due to lock wait timeout.")
                time.sleep(1)

    def test_save_requirements(self):
        user_id = 1  # Replace with valid user_id
        self.app.set_current_user(user_id)
        for option in self.dietary_screen.requirements_state:
            self.dietary_screen.requirements_state[option] = True
        self.dietary_screen.save_requirements()

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_requirements WHERE user_id = %s", (user_id,))
        requirements = cursor.fetchall()
        cursor.close()
        connection.close()
        self.assertGreater(len(requirements), 0, "Failed to save dietary requirements")

    def test_save_preferences(self):
        user_id = 1  # Replace with valid user_id
        self.app.set_current_user(user_id)
        for btn in self.preferences_screen.ids.preferences_grid.children:
            btn.state = 'down'
        self.preferences_screen.save_preferences()

        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM user_preferences WHERE user_id = %s", (user_id,))
        preferences = cursor.fetchall()
        cursor.close()
        connection.close()
        self.assertGreater(len(preferences), 0, "Failed to save preferences")

if __name__ == '__main__':
    unittest.main()
