from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
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
                rgba: 0, 0, 0, 1
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

class BorderedBox(BoxLayout):
    def __init__(self, **kwargs):
        super(BorderedBox, self).__init__(**kwargs)
        with self.canvas.before:
            # Outer black border
            Color(1, 1, 1, 1)
            self.outer_rect = Rectangle(size=self.size, pos=self.pos)
            # Inner white background
            Color(0, 0, 0, 1)
            self.inner_rect = Rectangle(size=(self.size[0] - 4, self.size[1] - 4), pos=(self.pos[0] + 2, self.pos[1] + 2))
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.outer_rect.size = instance.size
        self.outer_rect.pos = instance.pos
        self.inner_rect.size = (instance.size[0] - 4, instance.size[1] - 4)
        self.inner_rect.pos = (instance.pos[0] + 2, instance.pos[1] + 2)

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
        SELECT mi.id, mi.item_name, mi.description, mi.price, mi.category, mi.image_url,
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
        return [pref['preference'] for pref in preferences]

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
        user_data = ' '.join(user_preferences) + ' ' + user_requirements

        # Debug by printing user data
        print(f"User Data: {user_data}")

        # Filter items by user requirements
        filtered_items = [
            item for item in items
            if all(req.lower() in (item['description'] + ' ' + item['dietary_labels'] + ' ' + item['ingredients']).lower() for req in user_requirements.split())
        ]

        # Debug by printing filtered items
        print(f"Filtered items: {filtered_items}")

        # Only proceed if there are items after filtering
        if not filtered_items:
            print("No items match the user's dietary requirements.")
            return []

        descriptions = [
            item['description'] + ' ' + item['dietary_labels'] + ' ' + item['ingredients']
            for item in filtered_items
        ]

        # Debug by printing descriptions for vectorization
        print(f"Descriptions: {descriptions}")

        vectorizer = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        tfidf_matrix = vectorizer.fit_transform(descriptions)

        # Debug by printing tfidf_matrix shape
        print(f"TF-IDF Matrix shape: {tfidf_matrix.shape}")

        user_vector = vectorizer.transform([user_data])

        # Debug by printing user vector shape
        print(f"User Vector shape: {user_vector.shape}")

        cosine_sim = cosine_similarity(user_vector, tfidf_matrix)

        # Debug by printing cosine similarity scores
        print(f"Cosine Similarity: {cosine_sim}")

        # Weighting mechanism to prioritize the preferences
        preference_weights = [1.0 for _ in range(len(filtered_items))]
        for i, item in enumerate(filtered_items):
            item_data = item['description'] + ' ' + item['dietary_labels'] + ' ' + item['ingredients']
            for pref in user_preferences:
                if pref.lower() in item_data.lower() or item['category'].lower() == pref.lower():
                    preference_weights[i] *= 3.0  # Increase weight to match preferences with priority

        weighted_cosine_sim = cosine_sim[0] * preference_weights

        top_indices = weighted_cosine_sim.argsort()[-4:][::-1]
        recommended_items = [filtered_items[i] for i in top_indices]

        # Debug by printing recommended items
        print(f"Recommended Items: {recommended_items}")

        return recommended_items

    def display_recommendations(self, recommended_items):
        self.ids.grid.clear_widgets()
        for item in recommended_items:
            item_box = BorderedBox(orientation='vertical', size_hint=(1, None), height=100, padding=10)

            item_label = Label(
                text=f"{item['item_name']} - £{item['price']}",
                size_hint_y=None,
                color=(1, 1, 1, 1),  
                text_size=(self.width / 2 - 20, None),  
                halign='center',
                valign='middle'
            )
            item_label.bind(texture_size=item_label.setter('size'))

            item_box.add_widget(item_label)
            self.ids.grid.add_widget(item_box)

if __name__ == '__main__':
    class TestApp(App):
        current_user_id = None

        def build(self):
            return Home()

    TestApp().run()
