from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from database.session import get_db
from pydanticmodels.user import User as UserSchema
from models.user import User as UserModel 
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


passwordHash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

##pass helper word fucntions
def get_password_hash(plainPassword: str):
    return passwordHash.hash(plainPassword)

def verify_password(plainPassword: str, hashedPassword: str) -> bool:
    return passwordHash.verify(plainPassword, hashedPassword)


def is_password_strong(password: str) -> bool:
    return True

##mew user sign up function
def create_user(username: str, password: str, db: Session) -> bool:
    if does_user_exist(username, db):
        return False
    
    new_hashed_password = get_password_hash(password)
    db.add(UserModel(username=username, hashed_password=new_hashed_password))
    db.commit()
    return True


##existing user login
def does_username_password_match(username: str, password: str, db: Session) -> bool:
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return False
    return verify_password(password, user.hashed_password)

##check if username exists in the database
def does_user_exist(username: str, db: Session) -> bool:
    q = db.query(UserModel.username).filter(UserModel.username == username)
    return db.query(q.exists()).scalar()

def retrieve_user(username: str, db: Session) -> UserSchema | None:
    return db.query(UserModel).filter(UserModel.username == username).first() 


def create_access_token(username: str, expires_delta: timedelta | None = None):
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=int(TOKEN_EXPIRE_MINUTES)))
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    
## current logged in user    
async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user_normal)],
    db: Session = Depends(get_db)
):
    return current_user


async def get_current_user_normal(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> UserSchema:
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
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = retrieve_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user

