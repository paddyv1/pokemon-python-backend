from fastapi import APIRouter, Depends
from sqlalchemy import select
from database.session import get_db
from sqlalchemy.orm import Session

from models.user import User
router = APIRouter(prefix="/health")

@router.get("/db")
async def check_db(db: Session = Depends(get_db)):
    try:
        print("Checking database connection...")
        db.execute(select(User).order_by(User.id))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}