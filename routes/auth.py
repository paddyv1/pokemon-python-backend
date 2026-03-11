from fastapi import APIRouter

router = APIRouter()

@router.post("/register")
async def register():
    return {"todo": "Implement user registration"}

@router.post("/login")
async def login():
    return {"todo": "Implement user login"}

@router.get("/me")
async def get_current_user():
    return {"todo": "Implement get current user"}

