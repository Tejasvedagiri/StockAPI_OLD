from sqlalchemy import create_engine
import os
from sqlalchemy.inspection import inspect
from models.User import User
from models.StockTransaction import StockTransaction


db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_hostname = os.environ.get("DB_HOSTNAME")
db_port = os.environ.get("DB_PORT")
db_database = os.environ.get("DB_DATABASE")
db_type = os.environ.get("DB_TYPE")


if db_type == "MYSQL":
    DATABASE_URL = f'mysql+mysqlconnector://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_database}'
elif db_type == "POSG":
    DATABASE_URL = f'postgresql://{db_username}:{db_password}@{db_hostname}:{db_port}/{db_database}'
else:
    DATABASE_URL = "sqlite:///./test.db"

db = create_engine(DATABASE_URL, pool_recycle=3600)

if not inspect(db).has_table("Users"):
    User.__table__.create(bind=db)
if not inspect(db).has_table("StockTransaction"):
    StockTransaction.__table__.create(bind=db)

def get_database_engine():
    return db