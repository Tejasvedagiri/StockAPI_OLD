from sqlalchemy import create_engine
import os

db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_hostname = os.environ.get("DB_HOSTNAME")
db_port = os.environ.get("DB_PORT")
db_database = os.environ.get("DB_DATABASE")

if db_username:
    DATABASE_URL = f'postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_database}'
else:
    DATABASE_URL = "sqlite:///./test.db"

db = create_engine(DATABASE_URL)

def get_database_engine():
    return db