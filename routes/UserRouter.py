
from fastapi import APIRouter, Depends, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_database_engine
from sqlalchemy.orm import sessionmaker
from utils.Hash import Hash
from services.UserService import check_email_or_username_exists, insert_user

class DataLoaderDependencies:
    def __init__(self, db: Session = Depends(get_database_engine)):
        self.db = db
        self.session = sessionmaker(autocommit=False, autoflush=False, bind=db)()
        self.hasher = Hash(salt="SALT")

user_router = APIRouter(prefix="/user", dependencies=[Depends(get_database_engine)])


@user_router.post("/create_user", tags=["user"])
def create_user(username: str = Form(...),
        email: str = Form(...),
        password: str = Form(...), 
        deps: DataLoaderDependencies = Depends()
    ):
    if check_email_or_username_exists(deps, username, email):
        raise HTTPException(status_code=400, detail="Email already exists")
    else:

        return insert_user(deps, username, password, email)