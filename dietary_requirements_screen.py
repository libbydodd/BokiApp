from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty
from kivy.uix.togglebutton import ToggleButton
from kivy.metrics import dp
from kivy.app import App
import mysql.connector

DIETARY_OPTIONS = [
    'Vegan', 'Vegetarian', 'Pescatarian', 'Fish Allergy',
    'Lactose Intolerant', 'Gluten Free', 'Oat Milk', 'Coconut Milk',
    'Soya Milk', 'Nut Allergy', 'No Alcohol', 'Halal'
]

Builder.load_string("""
<DietaryRequirementsScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '15dp'
        padding: '30dp', '20dp', '30dp', '20dp'

        Image:
            source: 'logo.png'
            size_hint_y: None
            height: dp(60)
            keep_ratio: True
            allow_stretch: True

        Label:
            text: "Dietary Requirements"
            font_size: '24sp'
            size_hint_y: None
            height: '48dp'

        GridLayout:
            id: dietary_grid
            cols: 3
            spacing: '15dp'
            size_hint_y: None
            height: self.minimum_height
            size_hint_x: 0.9
            pos_hint: {'center_x': 0.5}

        Button:
            text: "Save Requirements"
            size_hint_y: None
            height: '48dp'
            background_color: 1, 0, 0, 1
            on_press: root.save_requirements()
""")

class DietaryRequirementsScreen(Screen):
    requirements_state = DictProperty({option: False for option in DIETARY_OPTIONS})

    def on_pre_enter(self):
        self.ids.dietary_grid.clear_widgets()
        button_width = dp(100)  # Set a fixed width for all buttons
        for option in DIETARY_OPTIONS:
            btn = ToggleButton(
                text=option,
                size_hint_y=None,
                width=button_width,  # Apply fixed width
                size_hint_x=0.9,  # Disable horizontal size hint
                height=dp(60),
                state='down' if self.requirements_state[option] else 'normal'
            )
            # Set text size to the button's width and unlimited height to allow for wrapping
            btn.text_size = (btn.width, None)
            # Align the text to the center
            btn.halign = 'center'
            btn.valign = 'middle'
            btn.bind(size=self.adjust_text_size, texture_size=self.adjust_text_size)
            btn.bind(on_release=self.toggle_requirement)
            self.ids.dietary_grid.add_widget(btn)

    def adjust_text_size(self, instance, value):
        # Adjust the text_size whenever the button size changes
        instance.text_size = (instance.width, None)

    def toggle_requirement(self, instance):
        self.requirements_state[instance.text] = (instance.state == 'down')

    def create_connection(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='Harryfreddie99!',  # Ensure password is correctly configured
            database='menu_database'
        )

    def save_requirements(self):
        selected_requirements = [req for req, selected in self.requirements_state.items() if selected]
        user_id = App.get_running_app().current_user_id
        if not user_id:
            print("User not logged in.")
            return

        connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM user_requirements WHERE user_id = %s", (user_id,))
            for requirement in selected_requirements:
                cursor.execute("SELECT label_id FROM dietary_labels WHERE label_name = %s", (requirement,))
                label_id = cursor.fetchone()
                if label_id:
                    cursor.execute("INSERT INTO user_requirements (user_id, label_id) VALUES (%s, %s)", (user_id, label_id[0]))
                else:
                    print(f"No label found for requirement: {requirement}")

            connection.commit()
            print("Selected dietary requirements updated successfully:", selected_requirements)
        except mysql.connector.Error as e:
            print(f"Failed to update dietary requirements: {e}")
        finally:
            cursor.close()
            connection.close()

        self.manager.current = 'preferences_screen'

if __name__ == '__main__':
    from kivy.app import App
    class TestApp(App):
        def build(self):
            return DietaryRequirementsScreen()

    TestApp().run()
