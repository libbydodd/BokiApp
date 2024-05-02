from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.togglebutton import ToggleButton

# Define the Kivy layout for your screen
kv = """
<PreferencesScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: '15dp'
        padding: '50dp', '50dp', '50dp', '50dp'

        Label:
            text: "Dietary Preferences"
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
            on_press: root.save_preferences()
"""

# Load the Kivy string first to ensure all IDs are available.
Builder.load_string(kv)

class PreferencesScreen(Screen):
    selected_preferences = ListProperty()

    def on_pre_enter(self):
        # Clear existing buttons
        self.ids.preferences_grid.clear_widgets()
        # Add new buttons based on preferences options
        for option in ['Breakfast', 'Lunch', 'Dinner', 'Drinks']:
            btn = ToggleButton(text=option, size_hint_y=None, height=40)
            self.ids.preferences_grid.add_widget(btn)

    def save_preferences(self):
        # Gather all selected dietary preferences
        self.selected_preferences = [btn.text for btn in self.ids.preferences_grid.children if btn.state == 'down']
        print("Selected dietary preferences:", self.selected_preferences)
        # This assumes that there's navigation logic to handle screen transitions
        self.manager.current = 'home'

# Below is only necessary if this script is run as a standalone file
if __name__ == '__main__':
    from kivy.app import App
    class TestApp(App):
        def build(self):
            return PreferencesScreen()

    TestApp().run()
