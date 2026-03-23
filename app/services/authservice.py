from datetime import datetime, timedelta, timezone
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.database.session import get_db
from app.pydanticmodels.auth import TokenData
from app.pydanticmodels.user import UserRead as UserSchema
from app.models.user import User as UserModel
from typing import Annotated
import jwt
from jwt.exceptions import InvalidTokenError
import os
from dotenv import load_dotenv
from fastapi import HTTPException, Depends, status
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

##fail fast here
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing. Add it to your .env file.")

ALGORITHM = os.getenv("ALGORITHM")
if not ALGORITHM:
    raise RuntimeError("ALGORITHM is missing. Add it to your .env file.")

TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
if not TOKEN_EXPIRE_MINUTES:
    raise RuntimeError(
        "ACCESS_TOKEN_EXPIRE_MINUTES is missing. Add it to your .env file."
    )

passwordHash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


##pass helper word fucntions
def get_password_hash(plainPassword: str):
    return passwordHash.hash(plainPassword)


def verify_password(plainPassword: str, hashedPassword: str) -> bool:
    return passwordHash.verify(plainPassword, hashedPassword)


def is_password_strong(password: str) -> bool:
    ##add real checks later
    return True


##mew user sign up function
def create_user(username: str, password: str, email: str, db: Session) -> bool:
    if does_user_exist(username, db):
        return False

    new_hashed_password = get_password_hash(password)
    db.add(
        UserModel(username=username, hashed_password=new_hashed_password, email=email)
    )
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
    userDetails = db.query(UserModel).filter(UserModel.username == username).first()
    if userDetails:
        return UserSchema(username=userDetails.username, user_id=userDetails.id)
    return None


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=int(TOKEN_EXPIRE_MINUTES))
    )
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


## current logged in user
async def get_current_active_user(
    current_user: Annotated[UserSchema, Depends(get_current_user_normal)],  # type: ignore
) -> UserSchema:
    return current_user


async def get_current_user_normal(
    token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)
) -> UserSchema:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("username")
        userId = payload.get("userId")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username, user_id=userId)
    except InvalidTokenError:
        raise credentials_exception
    user = retrieve_user(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user
