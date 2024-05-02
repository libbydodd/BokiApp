# home.py
import mysql.connector
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.image import AsyncImage

# Kivy layout definition
Builder.load_string("""
<Home>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 10
        padding: 10
        canvas.before:
            Color:
                rgba: 0, 0, 0, 1  # Black background
            Rectangle:
                pos: self.pos
                size: self.size

        Image:
            source: 'logo.png'
            size_hint: None, None
            size: 200, 200  # Adjust size as needed
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'Hello, welcome back!'
            size_hint_y: None
            height: 40
            color: 1, 1, 1, 1  # White text

        Label:
            text: 'You have no orders today.'
            size_hint_y: None
            height: 40
            color: 1, 1, 1, 1  # White text

        Button:
            text: 'View order history'
            size_hint: None, None
            size: 200, 40
            pos_hint: {'center_x': 0.5}
            background_color: 0.65, 0.07, 0.07, 1  # Red color

        Label:
            text: 'Recommended for you:'
            size_hint_y: None
            height: 40
            color: 1, 1, 1, 1  # White text

        GridLayout:
            id: recommendations_grid
            cols: 2
            size_hint_y: None
            height: self.minimum_height
            spacing: 10

        BoxLayout:
            size_hint_y: None
            height: 50
            pos_hint: {'bottom': 1}

            Button:
                text: 'Home'
            Button:
                text: 'Menu'
                on_press: root.manager.current = 'menu_touchpoints'
            Button:
                text: 'Basket'
                on_press: root.manager.current = 'basket'
            Button:
                text: 'Account'
                on_press: root.manager.current = 'account_screen'
""")

# Database connection and query functions
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',  # Adjust as necessary
        user='root',  # Your MySQL username
        password='Harryfreddie99!',  # Your MySQL password
        database='menu_database'  # Your MySQL database name
    )

def fetch_menu_items(dietary_labels, forbidden_ingredients):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    labels_placeholders = ', '.join(['%s'] * len(dietary_labels))
    ingredients_placeholders = ', '.join(['%s'] * len(forbidden_ingredients))

    query_labels = f"""
    SELECT DISTINCT mi.id, mi.item_name, mi.description, mi.price, mi.category
    FROM menu_items mi
    INNER JOIN menu_item_labels mil ON mi.id = mil.id
    INNER JOIN dietary_labels dl ON mil.label_id = dl.label_id
    WHERE dl.label_name IN ({labels_placeholders})
    """
    cursor.execute(query_labels, dietary_labels)
    items_matching_labels = cursor.fetchall()

    query_ingredients = f"""
    SELECT DISTINCT mii.id
    FROM menu_item_ingredients mii
    JOIN ingredients i ON mii.ingredient_id = i.ingredient_id
    WHERE i.ingredient IN ({ingredients_placeholders})
    """
    cursor.execute(query_ingredients, forbidden_ingredients)
    items_with_forbidden_ingredients = {item['id'] for item in cursor.fetchall()}

    filtered_items = [item for item in items_matching_labels if item['id'] not in items_with_forbidden_ingredients]

    conn.close()
    return filtered_items[:4]  # Return only the top 4 items

# Home Screen class
class Home(Screen):
    def on_enter(self):
        dietary_labels = ['vegan', 'gluten-free']  # Example labels
        forbidden_ingredients = ['nuts', 'dairy']  # Example forbidden ingredients
        recommendations = fetch_menu_items(dietary_labels, forbidden_ingredients)

        grid = self.ids.recommendations_grid
        grid.clear_widgets()
        for item in recommendations:
            image_path = f"images/{item['image']}"  # Adjust based on your image storage
            grid.add_widget(AsyncImage(source=image_path, size_hint_y=None, height=200))

# Main App class
if __name__ == '__main__':
    from kivy.app import App
    class TestApp(App):
        def build(self):
            return Home()

    TestApp().run()
