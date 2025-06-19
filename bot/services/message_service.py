"""Service layer for message CRUD operations."""

from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from ..models import Message, StatusEnum


def create_message(db: Session, user_id: int, text: str) -> Message:
    """Create a new message in pending status."""
    msg = Message(user_id=user_id, text=text)
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


def update_status(
    db: Session,
    message_id: int,
    status: StatusEnum,
    admin_id: Optional[int] = None,
) -> Optional[Message]:
    """Update message status and moderation info."""
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg:
        return None
    msg.status = status
    msg.moderated_at = datetime.utcnow()
    msg.admin_id = admin_id
    db.commit()
    db.refresh(msg)
    return msg


def get_message(db: Session, message_id: int) -> Optional[Message]:
    """Retrieve a message by ID."""
    return db.query(Message).filter(Message.id == message_id).first()
