from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta


class Hash:
    def __init__(self, rounds: int = 4, salt: str= "SALT"):
        self.rounds = rounds
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.salt = salt
        self.SECRET_KEY = "your-secret-key"
        self.ALGORITHM = "HS256"
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def hash(self, password: str):
        return self.pwd_context.hash(password+self.salt)

    def verify(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password+self.salt, hashed_password)
    
    def create_access_token(self, data: dict, ):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
 
def get_hasher():
    return Hash(salt="SALT")