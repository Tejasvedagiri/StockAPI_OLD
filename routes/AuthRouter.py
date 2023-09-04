from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import  OAuth2PasswordRequestForm

from models.User import UserModel, User
from services.UserService import authenticate_user
from services.AuthServices import get_current_active_user, create_new_access_token
from dependecies.AuthDependencies import AuthDependencies

auth_router = APIRouter()

@auth_router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), deps: AuthDependencies = Depends()):
    access_token, expiry_time = authenticate_user(form_data.username, form_data.password, deps)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"access_token": access_token, "token_type": "bearer", "expiry_time": expiry_time}


@auth_router.post("/token-refresh")
async def refresh_token(current_user: User = Depends(get_current_active_user), deps: AuthDependencies = Depends()):
    access_token, expiry_time = create_new_access_token(deps, current_user)
    return {"access_token": access_token, "token_type": "bearer", "expiry_time": expiry_time}

@auth_router.get("/users/me", response_model=UserModel)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user