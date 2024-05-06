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
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, item_name, description, price FROM menu_items")
            return cursor.fetchall()
        finally:
            cursor.close()
            connection.close()

    def fetch_user_preferences(self, user_id):
        connection = self.create_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT p.preference
                FROM user_preferences up
                JOIN preferences p ON up.preference_id = p.preference_id
                WHERE up.user_id = %s
            """, (user_id,))
            preferences = cursor.fetchall()
            return ' '.join([pref['preference'] for pref in preferences])
        finally:
            cursor.close()
            connection.close()

    def fetch_user_requirements(self, user_id):
        connection = self.create_connection()
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("""
                SELECT dl.label_name
                FROM user_requirements ur
                JOIN dietary_labels dl ON ur.label_id = dl.label_id
                WHERE ur.user_id = %s
            """, (user_id,))
            results = cursor.fetchall()
            return ' '.join([result['label_name'] for result in results])
        finally:
            cursor.close()
            connection.close()

    def recommend_items(self, user_id):
        items = self.fetch_menu_items()
        if not items:
            print("No items fetched from the database.")
            return []

        # Fetch and combine user preferences and requirements
        user_data = self.fetch_user_preferences(user_id) + ' ' + self.fetch_user_requirements(user_id)
        print("User Preferences and Requirements:", user_data)  # Debugging user data

        # Fetch and prepare menu item descriptions
        descriptions = [item['description'] for item in items]
        print("Menu Item Descriptions:", descriptions)  # Debugging menu item descriptions

        # Vectorization and cosine similarity calculation
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(descriptions)
        user_vector = vectorizer.transform([user_data])
        cosine_sim = cosine_similarity(user_vector, tfidf_matrix)

        # Identifying top recommendations
        top_indices = cosine_sim[0].argsort()[-4:][::-1]
        return [items[i] for i in top_indices]

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
