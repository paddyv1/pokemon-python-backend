from datetime import datetime
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from app.models.base import Base
from typing import List

class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    
    teams: Mapped[List["Team"]] = relationship(  # noqa: F821 # type: ignore
        back_populates="user",
        cascade="all, delete-orphan",
    )