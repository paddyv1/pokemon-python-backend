from datetime import timedelta
from app.pydanticmodels.auth import TokenResponse
from fastapi import APIRouter
from app.database.session import get_db
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.pydanticmodels.user import UserRead, RegisterRequest
from app.services.authservice import create_access_token, retrieve_user, create_user, does_user_exist, get_current_active_user, is_password_strong, does_username_password_match
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")
TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    if not is_password_strong(request.password):
        return {"error": "Password is not strong enough"}
    if does_user_exist(request.username, db):
        return {"error": "User already exists"}
    if create_user(request.username, request.password, db):
        return {"message": "User registered successfully"}
    return {"error": "Failed to register user"}

@router.post("/login")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    user = form_data.username
    if not does_user_exist(user, db):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not does_username_password_match(user, form_data.password, db):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=int(TOKEN_EXPIRE_MINUTES))
    usermodel = retrieve_user(user, db)
    access_token = create_access_token(
        data={"sub": usermodel.username}, expires_delta=access_token_expires
    )
    
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post("/logout")
async def logout():
    return {"message": "Logged out. Delete token on client."} #frontend will delete token from headers

@router.get("/me")
async def read_users_me(
    current_user: Annotated[UserRead, Depends(get_current_active_user)]
) -> UserRead:
    return current_user

