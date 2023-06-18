from passlib.context import CryptContext
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional
from jose import jwt
import datetime
import redis
from sql.client import Client
from models.user_client import UserClient
from models import User

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserManager:
    def __init__(self):
        print('UserManager Created')
        self.user_client = UserClient(Client())
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.redis_client = redis.Redis(
            host='your_elasticache_redis_endpoint',  # Replace with your ElastiCache cluster endpoint
            port=6379,  # Default Redis port
            decode_responses=True)
        
    def create_user(self, ID, PW, second_PW, storeUID,phone,wallet ):
        self.user_client.create(ID, PW, second_PW, storeUID,phone,wallet)

    def authenticate_user(self, username: str, password: str):
        # Implement this function to verify username and password with your database
        user = self.get_user(username)
        if not user:
            return None
        if not self.verify_password(password, user.PW):
            return None
        return user

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def get_user(self, username: str) -> Optional[User]:
        # Assume the `userUID` is the username
        user_tuple = self.user_client.read(username)
        if user_tuple is None:
            return None
        return User(*user_tuple)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = self.authenticate_user(form_data.username, form_data.password)
        if user is None:
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = self.create_access_token(data={"sub": user.username})
        return {"access_token": access_token, "token_type": "bearer"}

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            if username is None:
                raise credentials_exception
        except jwt.PyJWTError:
            raise credentials_exception
        return username
    
    def blacklist_token(self, token: str):
        self.redis_client.set(token, 'blacklisted')

    def is_token_blacklisted(self, token: str):
        return self.redis_client.exists(token)