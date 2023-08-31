from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import os

user_name = os.environ.get("API_USERNAME")
password = os.environ.get("API_PASSWORD")
users_db = {
    user_name : password
}
security = HTTPBasic()

# Define a dependency function to verify user credentials
def get_current_user(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username not in users_db and credentials.password == users_db[credentials.username]:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username