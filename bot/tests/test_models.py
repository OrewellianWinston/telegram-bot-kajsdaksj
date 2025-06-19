"""Tests for ORM models."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db import Base
from ..models import Message, StatusEnum


def setup_in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, TestingSessionLocal


def test_message_creation():
    engine, Session = setup_in_memory_db()
    with Session() as db:
        msg = Message(user_id=1, text="hi")
        db.add(msg)
        db.commit()
        db.refresh(msg)
        assert msg.id == 1
        assert msg.status == StatusEnum.pending
