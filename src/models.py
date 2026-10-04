import uuid
from datetime import datetime

from sqlalchemy import DateTime, Text, Uuid, func
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from src.db import Base


class StringCache(Base):
    """One row per distinct input string: original -> transformed."""

    __tablename__ = "string_cache"

    string_hash: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    original: Mapped[str] = mapped_column(Text, nullable=False)
    transformed_string: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class ListCache(Base):
    """One row per distinct input list: list_hash -> list of transformed strings."""

    __tablename__ = "list_cache"

    list_hash: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True)
    transformed: Mapped[list[str]] = mapped_column(ARRAY(Text), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )