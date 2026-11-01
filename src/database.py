import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Access the variables
db_url = os.getenv("DATABASE_URL")

print(db_url)