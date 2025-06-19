"""Tests for user flow without Telegram network."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db import Base
from ..services.message_service import create_message


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, TestingSessionLocal


def test_user_message_pending():
    engine, Session = setup_db()
    with Session() as db:
        msg = create_message(db, user_id=1, text="hello")
        assert msg.status.value == "pending"
        assert msg.user_id == 1
