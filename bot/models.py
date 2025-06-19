"""SQLAlchemy ORM models for the moderation bot."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from .db import Base


class StatusEnum(str, Enum):
    """Status for a moderated message."""

    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Message(Base):
    """Message submitted by a user for moderation."""

    __tablename__ = "messages"

    id: int = Column(Integer, primary_key=True, index=True)
    user_id: int = Column(Integer, nullable=False)
    text: str = Column(String, nullable=False)
    status: StatusEnum = Column(
        SAEnum(StatusEnum), default=StatusEnum.pending, nullable=False
    )
    created_at: datetime = Column(DateTime, default=datetime.utcnow, nullable=False)
    moderated_at: Optional[datetime] = Column(DateTime, nullable=True)
    admin_id: Optional[int] = Column(Integer, ForeignKey("admins.id"), nullable=True)


class Admin(Base):
    """Admin user who moderates messages."""

    __tablename__ = "admins"

    id: int = Column(Integer, primary_key=True)
    telegram_id: int = Column(Integer, unique=True, nullable=False)
    messages = relationship("Message", backref="admin")
