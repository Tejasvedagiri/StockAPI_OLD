from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_database_engine
from sqlalchemy.orm import sessionmaker
from utils.Hash import get_hasher


class AuthDependencies:
    def __init__(self, db: Session = Depends(get_database_engine), hasher: Session = Depends(get_hasher)):
        self.db = db
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=db)()
        self.hasher = hasher