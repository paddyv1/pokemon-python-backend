from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

##fix before commiting code
engine = create_engine("postgresql://postgres:pokemonshowdowndatabase@db.stkqfrnaprazgazuykpk.supabase.co:5432/postgres")

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