from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import DictProperty
from kivy.uix.togglebutton import ToggleButton

# Add your options for the dietary requirements
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
        padding: '50dp', '50dp', '50dp', '50dp'

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

        Button:
            text: "Save Requirements"
            size_hint_y: None
            height: '48dp'
            on_press: root.save_requirements()
""")

class DietaryRequirementsScreen(Screen):
    # Using a dictionary to keep track of button states
    requirements_state = DictProperty({option: False for option in DIETARY_OPTIONS})

    def on_pre_enter(self):
        self.ids.dietary_grid.clear_widgets()  # Clear existing buttons
        for option in DIETARY_OPTIONS:
            btn = ToggleButton(
                text=option, 
                size_hint_y=None, 
                height=40,
                state='down' if self.requirements_state[option] else 'normal'
            )
            btn.bind(on_release=self.toggle_requirement)
            self.ids.dietary_grid.add_widget(btn)

    def toggle_requirement(self, instance):
        # Toggle the state in the dictionary when the button is pressed
        self.requirements_state[instance.text] = (instance.state == 'down')

    def save_requirements(self):
        # Gather all selected dietary requirements based on stored states
        selected_requirements = [req for req, selected in self.requirements_state.items() if selected]
        print("Selected dietary requirements:", selected_requirements)
        # Navigate to the next screen or save the preferences
        self.manager.current = 'preferences_screen'

if __name__ == '__main__':
    from kivy.app import App
    class TestApp(App):
        def build(self):
            return DietaryRequirementsScreen()

    TestApp().run()
