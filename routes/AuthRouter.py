from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import  OAuth2PasswordRequestForm

from models.User import UserModel, User
from services.UserService import authenticate_user
from services.AuthServices import get_current_active_user
from dependecies.AuthDependencies import AuthDependencies

auth_router = APIRouter()

@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), deps: AuthDependencies = Depends()):
    access_token = authenticate_user(form_data.username, form_data.password, deps)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": access_token, "token_type": "bearer"}

@auth_router.get("/users/me", response_model=UserModel)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user