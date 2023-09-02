from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from services.UserService import get_user_details_from_username
from dependecies.AuthDependencies import AuthDependencies


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_active_user(token: str = Depends(oauth2_scheme), deps: AuthDependencies = Depends()):
    try:
        payload = jwt.decode(token, deps.hasher.SECRET_KEY, algorithms=[deps.hasher.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=400, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = get_user_details_from_username(deps=deps, username=username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user