# main.py
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from login_screen import LoginScreen
from register_screen import RegisterScreen
from dietary_requirements_screen import DietaryRequirementsScreen
from preferences_screen import PreferencesScreen
from home import Home
from menu_touchpoints import MenuTouchpoints
from collection_time import CollectionTime
from boki_menu import BokiMenu 
from basket import Basket

class MyApp(App):
    current_user_id = None  # Track the current user's ID

    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        self.basket = []  # Initialize an empty list to hold basket items
            
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(LoginScreen(name='login_screen'))
        self.sm.add_widget(RegisterScreen(name='register_screen'))
        self.sm.add_widget(DietaryRequirementsScreen(name='dietary_requirements_screen'))
        self.sm.add_widget(PreferencesScreen(name='preferences_screen'))
        self.sm.add_widget(Home(name='home'))
        self.sm.add_widget(MenuTouchpoints(name='menu_touchpoints'))
        self.sm.add_widget(CollectionTime(name='collection_time'))
        self.sm.add_widget(BokiMenu(name='boki_menu'))
        self.sm.add_widget(Basket(name='basket'))
        self.sm.current = 'login_screen'
        return self.sm

    def add_item_to_basket(self, item):
        """Method to add an item to the basket."""
        self.basket.append(item)
        print(f"Added {item['name']} to basket")

    def set_current_user(self, user_id):
        """ Set the current logged-in user ID """
        self.current_user_id = user_id
        print(f"Current User ID: {self.current_user_id}")

if __name__ == '__main__':
    MyApp().run()
