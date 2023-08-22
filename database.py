from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
DATABASE_URL = "sqlite:///./test.db"

db = create_engine(DATABASE_URL)

def get_database_engine():
    return db