from fastapi import APIRouter
from database.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session
from services.authservice import create_user, does_user_exist, verify_password, is_password_strong

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(username: str, password: str, db: Session = Depends(get_db)):
    if not is_password_strong(password):
        return {"error": "Password is not strong enough"}
    if does_user_exist(username):
        return {"error": "User already exists"}
    if create_user(username, password, db):
        return {"message": "User registered successfully"}
    return {"error": "Failed to register user"}

@router.post("/login")
async def login():
    return {"todo": "Implement user login"}

@router.post("/logout")
async def logout():
    return {"todo": "Implement user logout"}

@router.get("/me")
async def get_current_user():
    return {"todo": "Implement get current user"}

