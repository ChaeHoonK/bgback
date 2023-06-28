from fastapi import FastAPI, Depends, HTTPException, status, Response
import socketio
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Optional
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from models import init_all
from library.jwt import create_access_token
from base_models import Token, Auction as AuctionBM, Request as RequestBM, RequestStatus
from facade.auction_facade import AuctionFacade


app = FastAPI()


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
async def startup_event():
    sio = socketio.AsyncServer(async_mode='asgi')
    app.mount('/', socketio.ASGIApp(sio))
    init_all()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post('/auction')
async def auction_create(auction: AuctionBM):
    AuctionFacade().create_auction(*auction)

@app.post('/request')
async def request_create(request: RequestBM):
    AuctionFacade().create_request(*request)
    # notify the receiver(request.receiver_user_uid)

@app.patch('/request')
async def handle_request(request_status: RequestStatus):
    manager= AuctionFacade()
    
    manager.process_request(**request_status)

# @app.on_event("startup")
# async def startup():
#     await database.connect()

# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


# @app.post("/signup")
# def signup(ID: str, PW: str, store_UID: Optional[int], second_PW: str, phone: str, wallet: Optional[list[str]]):
#     user_manager = UserManager()

#     # hash the password
#     hashed_password = user_manager.get_password_hash(PW)

#     # create the user
#     user_manager.create_user(ID=ID, PW=hashed_password, storeUID=store_UID,
#                              second_PW=second_PW, phone=phone, wallet=[])

#     return {"detail": "User created"}


# @app.post("/token", response_model=Token)
# def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
#     user_manager = UserManager()

#     user = user_manager.authenticate_user(
#         form_data.username, form_data.password)

#     if user is None:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     response.set_cookie(key="access_token",
#                         value=f"Bearer {access_token}", httponly=True)

#     return {"access_token": access_token, "token_type": "bearer"}


# @app.post("/logout")
# async def logout(response: Response):
#     response.delete_cookie("access_token")
#     return {"message": "User logged out successfully"}


# @app.get("/users/me/")
# async def read_users_me(token: str = Depends(oauth2_scheme)):
#     return {"username": token}



