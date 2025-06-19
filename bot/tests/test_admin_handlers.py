"""Tests for admin moderation flow."""

from unittest.mock import AsyncMock

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..db import Base
from ..services.message_service import create_message, update_status
from ..services import publish_service
from ..models import StatusEnum


def setup_db():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return engine, TestingSessionLocal


async def test_admin_approve_flow(monkeypatch):
    engine, Session = setup_db()
    with Session() as db:
        monkeypatch.setattr(publish_service, "publish_to_channel", mock_publish)
        mock_publish = AsyncMock()
        updated = update_status(db, msg.id, StatusEnum.approved, admin_id=2)
        await publish_service.publish_to_channel(None, updated.text)
        assert updated.status == StatusEnum.approved
        mock_publish.assert_awaited()


def test_admin_reject_flow():
    engine, Session = setup_db()
    with Session() as db:
        msg = create_message(db, user_id=1, text="hello")
        updated = update_status(db, msg.id, StatusEnum.rejected, admin_id=2)
        assert updated.status == StatusEnum.rejected
