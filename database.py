from sqlalchemy import create_engine
import os
DATABASE_URL = "sqlite:///./test.db"

db = create_engine(DATABASE_URL)

def get_database_engine():
    return db