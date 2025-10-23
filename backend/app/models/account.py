from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import TEXT, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.config import Base
from app.models.enums import Provider

if TYPE_CHECKING:
    from app.models.user import UserModel


class AccountModel(Base):
    __tablename__ = "account"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    provider: Mapped[Provider] = mapped_column(
        Enum(Provider, name="provider_type", values_callable=lambda x: [e.value for e in x]), nullable=False
    )
    provider_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_url: Mapped[str | None] = mapped_column(TEXT, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default="now()")
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default="now()", onupdate="now()"
    )

    user: Mapped[UserModel] = relationship(back_populates="account", lazy="joined")
