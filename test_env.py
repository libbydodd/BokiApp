from dotenv import load_dotenv
import os

load_dotenv()  # Ensure this is executed before accessing environment variables

print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("DB_DATABASE:", os.getenv('DB_DATABASE'))
