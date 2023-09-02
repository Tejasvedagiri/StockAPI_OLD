
from models.User import User
import uuid
from dependecies.AuthDependencies import AuthDependencies

def authenticate_user(username: str, password: str, deps: AuthDependencies ):
    user = get_user_details_from_username(deps=deps, username=username)
    if not user or not deps.hasher.verify(password, user.Password):
        return None
    access_token = deps.hasher.create_access_token(data={"sub": user.UserName})
    return access_token

def get_user_details_from_username(deps, username):
    user = deps.session.query(User).filter(User.UserName == username).first()
    if user is not None:
        user_object = User(
            ID=user.ID,
            UserName=user.UserName,
            Email=user.Email,
            Password=user.Password
        )
        return user_object
    return None

def check_email_or_username_exists(deps, username, email):
    return deps.session.query(User).filter(User.UserName == username and User.Email == email).first() is not None 

def insert_user(deps, username, password, email):
    user =  User(
            ID=str(uuid.uuid4()),
            UserName=username,
            Email=email,
            Password=deps.hasher.hash(password=password),
        )
    deps.session.add(user)
    deps.session.commit()
    return True