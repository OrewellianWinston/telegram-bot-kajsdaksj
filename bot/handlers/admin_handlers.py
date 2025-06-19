"""Handlers for admin actions via callback queries."""

from aiogram import types, Dispatcher

from ..db import SessionLocal
from ..services.message_service import update_status
from ..services.publish_service import publish_to_channel
from ..models import StatusEnum


def register_admin_handlers(dp: Dispatcher) -> None:
    """Register admin callback handlers."""

    @dp.callback_query_handler(lambda c: c.data.startswith("approve"))
    async def approve(call: types.CallbackQuery) -> None:
        _, msg_id = call.data.split(":")
        message_id = int(msg_id)
        with SessionLocal() as db:
            msg = update_status(
                db,
                message_id=message_id,
                status=StatusEnum.approved,
                admin_id=call.from_user.id,
            )
        if msg:
            await publish_to_channel(call.bot, msg.text)
            await call.message.edit_text(f"✅ Approved message #{message_id}")
        await call.answer()

    @dp.callback_query_handler(lambda c: c.data.startswith("reject"))
    async def reject(call: types.CallbackQuery) -> None:
        _, msg_id = call.data.split(":")
        message_id = int(msg_id)
        with SessionLocal() as db:
            update_status(
                db,
                message_id=message_id,
                status=StatusEnum.rejected,
                admin_id=call.from_user.id,
            )
        await call.message.edit_text(f"❌ Rejected message #{message_id}")
        await call.answer()
