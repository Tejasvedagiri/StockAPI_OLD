from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_database_engine
from sqlalchemy.orm import sessionmaker
from utils.Hash import get_hasher
from models.User import User
from services.AuthServices import get_current_active_user
from utils.Hash import Hash

class DataDependencies:
    def __init__(self, db: Session = Depends(get_database_engine), hasher: Session = Depends(get_hasher), 
                 user: User = Depends(get_current_active_user)):
        self.db = db
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=db)()
        self.hasher: Hash  = hasher
        self.user: User = user