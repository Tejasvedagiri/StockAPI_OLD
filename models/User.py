import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import CHAR  # Use the appropriate UUID type for MySQL
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel


Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'  # Set the table name
    ID = Column(CHAR(36), primary_key=True, default=str(uuid.uuid4()), unique=True, index=True)
    UserName = Column(String, index=True)
    Email = Column(String, unique=True, index=True)
    Password = Column(String)
    
class UserModel(BaseModel):
    ID: str
    UserName: str
    Email: str
    Password: str