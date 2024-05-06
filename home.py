from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import mysql.connector

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
            size: 200, 200
            pos_hint: {'center_x': 0.5}

        Label:
            text: 'Hello, welcome back!'
            size_hint_y: None
            height: 40
            color: 1, 1, 1, 1

        Label:
            text: 'You have no orders today.'
            size_hint_y: None
            height: 40
            color: 1, 1, 1, 1

        Button:
            text: 'View order history'
            size_hint: None, None
            size: 200, 40
            pos_hint: {'center_x': 0.5}
            background_color: 0.65, 0.07, 0.07, 1

        Label:
            text: 'Recommended for you:'
            size_hint_y: None
            height: 40
            color: 1, 1, 1, 1

        GridLayout:
            id: grid
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

class Home(Screen):
    def on_enter(self):
        user_id = App.get_running_app().current_user_id
        if user_id is not None:
            recommended_items = self.recommend_items(user_id)
            self.display_recommendations(recommended_items)
        else:
            print("No user logged in!")

    def create_connection(self):
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='Harryfreddie99!',
            database='menu_database'
        )

    def fetch_menu_items(self):
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
        SELECT mi.id, mi.item_name, mi.description, mi.price,
            GROUP_CONCAT(DISTINCT d.label_name SEPARATOR ', ') AS dietary_labels,
            GROUP_CONCAT(DISTINCT ing.ingredient SEPARATOR ', ') AS ingredients
        FROM menu_items mi
        LEFT JOIN menu_item_labels mil ON mi.id = mil.id  
        LEFT JOIN dietary_labels d ON mil.label_id = d.label_id
        LEFT JOIN menu_item_ingredients mii ON mi.id = mii.id  
        LEFT JOIN ingredients ing ON mii.ingredient_id = ing.ingredient_id
        GROUP BY mi.id
        """
        cursor.execute(query)
        items = cursor.fetchall()
        cursor.close()
        connection.close()
        return items


    def fetch_user_preferences(self, user_id):
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT p.preference
            FROM user_preferences up
            JOIN preferences p ON up.preference_id = p.preference_id
            WHERE up.user_id = %s
        """, (user_id,))
        preferences = cursor.fetchall()
        cursor.close()
        connection.close()
        return ' '.join([pref['preference'] for pref in preferences])

    def fetch_user_requirements(self, user_id):
        connection = self.create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT dl.label_name
            FROM user_requirements ur
            JOIN dietary_labels dl ON ur.label_id = dl.label_id
            WHERE ur.user_id = %s
        """, (user_id,))
        requirements = cursor.fetchall()
        cursor.close()
        connection.close()
        return ' '.join([req['label_name'] for req in requirements])

    def recommend_items(self, user_id):
        items = self.fetch_menu_items()
        user_preferences = self.fetch_user_preferences(user_id)
        user_requirements = self.fetch_user_requirements(user_id)

        # Combine user data for vectorization
        user_data = ' '.join(user_preferences + user_requirements)

        # Filter items by user preferences and requirements
        filtered_items = [item for item in items if all(req in item['description'] or req in item['dietary_labels'] or req in item['ingredients'] for req in user_requirements)]

        # Only proceed if there are items after filtering
        if not filtered_items:
            print("No items match the user's dietary requirements.")
            return []

        descriptions = [item['description'] + ' ' + item['dietary_labels'] + ' ' + item['ingredients'] for item in filtered_items]
        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        user_vector = vectorizer.transform([user_data])
        cosine_sim = cosine_similarity(user_vector, tfidf_matrix)

        top_indices = cosine_sim[0].argsort()[-4:][::-1]
        recommended_items = [filtered_items[i] for i in top_indices]

        return recommended_items

    def display_recommendations(self, recommended_items):
        self.ids.grid.clear_widgets()
        for item in recommended_items:
            item_label = Label(text=f"{item['item_name']} - £{item['price']}", size_hint_y=None, height=40, color=(1, 1, 1, 1))
            self.ids.grid.add_widget(item_label)

if __name__ == '__main__':
    class TestApp(App):
        current_user_id = None

        def build(self):
            return Home()

    TestApp().run()
