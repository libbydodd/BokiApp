import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import Error

# Load environment variables from .env file
load_dotenv()

def create_connection():
    """Create a database connection and return the connection object."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            port=3306,
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL Platform: {e}")
        return None


def fetch_menu_items():
    """Fetch all menu items from the database."""
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM menu_items")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return records
    else:
        return []

# Example usage
if __name__ == "__main__":
    items = fetch_menu_items()
    print(items)
