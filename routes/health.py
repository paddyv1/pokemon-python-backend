from fastapi import APIRouter, Depends
from sqlalchemy import text
from database.session import get_db
from sqlalchemy.orm import Session
router = APIRouter(prefix="/health")

@router.get("/db")
async def check_db(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}