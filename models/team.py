# models/team.py
from datetime import datetime
from typing import List
from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    team_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="teams")  # type: ignore # noqa: F821

    slots: Mapped[List["Slot"]] = relationship(  # type: ignore  # noqa: F821
        back_populates="team",
        cascade="all, delete-orphan",
    )

    create_date: Mapped[datetime] = mapped_column(insert_default=func.now())
    updated_date: Mapped[datetime] = mapped_column(
        insert_default=func.now(),
        onupdate=func.now(),
    )