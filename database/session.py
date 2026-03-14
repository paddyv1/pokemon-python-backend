import os

from dotenv import load_dotenv
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")
SUPABASE_STRING = os.getenv("SUPABASE_STRING")
##fix before commiting code
engine = create_engine(SUPABASE_STRING)

Session = sessionmaker(engine)

def get_db():
    db = Session()
    try:
        yield db
    except Exception as e:
        ##improve this to logging
        print(e)
        db.rollback()
        raise
    finally:
        db.close()