from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from decimal import Decimal
from datetime import datetime
import mysql.connector

# Define the Kivy layout using the Builder
KV = """
<CheckoutScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10

        Image:
            source: 'logo.png'
            size_hint_y: None
            height: '60dp'
            keep_ratio: True
            allow_stretch: True

        Label:
            text: 'Checkout'
            font_size: '24sp'
            size_hint_y: None
            height: 50

        ScrollView:
            size_hint_y: None
            height: 300
            BoxLayout:
                id: items_box
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

        Label:
            id: total_label
            text: 'Total: £0.00'
            font_size: '20sp'
            size_hint_y: None
            height: 40

        BoxLayout:
            size_hint_y: None
            height: 50
            spacing: 10

            Button:
                text: 'Cancel'
                on_press: root.manager.current = 'home'

            Button:
                text: 'Complete Purchase'
                background_color: 1, 0, 0, 1
                on_press: root.complete_purchase()
"""

# Load the string into the Kivy Builder
Builder.load_string(KV)

class CheckoutScreen(Screen):
    def on_pre_enter(self):
        self.ids.items_box.clear_widgets()
        total = Decimal('0.00')  # Initialize total as a Decimal
        basket_items = App.get_running_app().basket

        for item in basket_items:
            item_price = Decimal(item['price'])  # Ensure price is a Decimal
            label_text = f"{item['item_name']} - £{item_price:.2f}"
            label = Label(text=label_text, size_hint_y=None, height=30)
            self.ids.items_box.add_widget(label)
            total += item_price

        self.ids.total_label.text = f"Total: £{total:.2f}"

    def complete_purchase(self):
        basket_items = App.get_running_app().basket
        if not basket_items:
            print("No items to purchase!")
            return
        
        try:
            connection = self.create_connection()
            cursor = connection.cursor()
            user_id = App.get_running_app().current_user_id  # Assuming there's a user ID to track who is making the purchase
            total = sum(Decimal(item['price']) for item in basket_items)
            order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            order_query = """
                INSERT INTO orders (user_id, order_date, total, status)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(order_query, (user_id, order_date, float(total), 'Pending'))
            
            connection.commit()
            cursor.close()
            connection.close()
            App.get_running_app().basket.clear()
            self.manager.current = 'home'
            print("Purchase completed and saved to database!")
        except mysql.connector.Error as e:
            print("Error saving purchase to database:", e)

    def create_connection(self):
        return mysql.connector.connect(
            host='localhost', 
            user='root', 
            password='Harryfreddie99!', 
            database='menu_database'
        )

class HomeScreen(Screen):
    pass

class MyApp(App):
    def build(self):
        self.basket = [{'item_name': 'Item 1', 'price': 29.99}, {'item_name': 'Item 2', 'price': 49.99}]
        sm = ScreenManager()
        sm.add_widget(HomeScreen(name='home'))
        sm.add_widget(CheckoutScreen(name='checkout'))
        return sm

if __name__ == '__main__':
    MyApp().run()
