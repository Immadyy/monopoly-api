import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Load the .env file
load_dotenv()

# Access the variables
db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url, echo=True)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass