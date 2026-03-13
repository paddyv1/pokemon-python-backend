from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from models.user import User


passwordHash = PasswordHash.recommended()


##pass word fucntions
def get_password_hash(plainPassword: str):
    return passwordHash.hash(plainPassword)

def verify_password(plainPassword: str, hashedPassword: str) -> bool:
    return passwordHash.verify(plainPassword, hashedPassword)

def is_password_strong(password: str) -> bool:
    return True

##user fucntions
def create_user(username: str, password: str, db: Session) -> bool:
    if does_user_exist(username):
        return False
    
    new_hashed_password = get_password_hash(password)
    db.add(User(username=username, hashed_password=new_hashed_password))
    db.commit()
    return True

def does_user_exist(username: str) -> bool:
    return False



