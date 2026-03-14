from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from app.models.base import Base

class Slot(Base):
    __tablename__ = "slots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pkdex_number: Mapped[int] = mapped_column(nullable=False)
    pk_name: Mapped[str] = mapped_column(String(50), nullable=False)

    team_id: Mapped[int] = mapped_column(ForeignKey("teams.id"), nullable=False)
    team: Mapped["Team"] = relationship(back_populates="slots")  # type: ignore # noqa: F821

    __table_args__ = (
        CheckConstraint("pkdex_number BETWEEN 0 AND 1025", name="chk_pkdex_number_range"),
    )