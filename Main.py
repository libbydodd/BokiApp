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
    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterScreen(name='register_screen'))
        sm.add_widget(DietaryRequirementsScreen(name='dietary_requirements_screen'))
        sm.add_widget(PreferencesScreen(name='preferences_screen'))
        sm.add_widget(Home(name='home'))
        sm.add_widget(MenuTouchpoints(name='menu_touchpoints'))
        sm.add_widget(CollectionTime(name='collection_time'))
        sm.add_widget(BokiMenu(name='boki_menu')) 
        sm.add_widget(Basket(name='basket'))
        sm.current = 'login'
        return sm

if __name__ == '__main__':
    MyApp().run()
