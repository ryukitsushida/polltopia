from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.config import Base


class SampleModel(Base):
    __tablename__ = "sample"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
