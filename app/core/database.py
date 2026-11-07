import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

Base = declarative_base()

class DatabaseManager:
    def __init__(self, db_url: str | None = None):
        self.db_url = db_url or os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("Database URL must be provided or set in environment variables.")
        
        self.engine = create_engine(self.db_url, echo=False)
        self.sessionlocal = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)

    def get_db(self):
        db = self.sessionlocal()
        try:
            yield db
        finally:
            db.close()

db_manager = DatabaseManager()