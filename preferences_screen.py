#preferences_screen.py
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.app import App
import mysql.connector

kv = """
<PreferencesScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '15dp'
        padding: '50dp', '50dp', '50dp', '50dp'

        Image:
            source: 'logo.png'
            size_hint_y: None
            height: dp(60)
            keep_ratio: True
            allow_stretch: True

        Label:
            text: "Preferences"
            font_size: '24sp'
            size_hint_y: None
            height: '48dp'

        GridLayout:
            id: preferences_grid
            cols: 3
            spacing: '15dp'
            size_hint_y: None
            height: self.minimum_height

        Button:
            text: "Save Preferences"
            size_hint_y: None
            height: '48dp'
            background_color: 1, 0, 0, 1
            on_press: root.save_preferences()
"""

Builder.load_string(kv)

class PreferencesScreen(Screen):
    def on_pre_enter(self):
        self.ids.preferences_grid.clear_widgets()
        for option in ['Breakfast', 'Lunch', 'Dinner', 'Snacks', 'Drinks']:
            btn = ToggleButton(text=option, size_hint_y=None, height=40)
            self.ids.preferences_grid.add_widget(btn)

    def create_connection(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='Harryfreddie99!', 
            database='menu_database'
        )

    def save_preferences(self):
        selected_preferences = [btn.text for btn in self.ids.preferences_grid.children if btn.state == 'down']
        print("Selected preferences:", selected_preferences)
        user_id = App.get_running_app().current_user_id
        if user_id:
            conn = self.create_connection()
            cursor = conn.cursor()
            try:
                cursor.execute("DELETE FROM user_preferences WHERE user_id = %s", (user_id,))
                for preference in selected_preferences:
                    cursor.execute("SELECT preference_id FROM preferences WHERE preference = %s", (preference,))
                    preference_id = cursor.fetchone()
                    if preference_id:
                        cursor.execute("INSERT INTO user_preferences (user_id, preference_id) VALUES (%s, %s)", (user_id, preference_id[0]))
                    else:
                        print(f"No ID found for preference: {preference}")
                conn.commit()
            except mysql.connector.Error as e:
                print(f"Database error: {e}")
            finally:
                cursor.close()
                conn.close()
                self.manager.current = 'home'

if __name__ == '__main__':
    class TestApp(App):
        def build(self):
            return PreferencesScreen()

    TestApp().run()
