"""Aiogram handlers for regular users."""

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ..db import SessionLocal
from ..services.message_service import create_message, get_message
from ..config import settings


def register_user_handlers(dp: Dispatcher) -> None:
    """Register user-facing command and message handlers."""

    @dp.message_handler(commands=["start"])
    async def start(message: types.Message) -> None:
        await message.answer("Welcome! Send me a message to submit for review.")

    @dp.message_handler(commands=["status"])
    async def status(message: types.Message) -> None:
        parts = message.text.split()
        if len(parts) != 2 or not parts[1].isdigit():
            await message.answer("Usage: /status <message_id>")
            return
        message_id = int(parts[1])
        with SessionLocal() as db:
            msg = get_message(db, message_id)
            if not msg or msg.user_id != message.from_user.id:
                await message.answer("Message not found.")
                return
            await message.answer(f"Status: {msg.status}")

    @dp.message_handler(content_types=types.ContentType.TEXT)
    async def receive_text(message: types.Message) -> None:
        with SessionLocal() as db:
            msg = create_message(db, user_id=message.from_user.id, text=message.text)

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Approve", callback_data=f"approve:{msg.id}"
                    ),
                    InlineKeyboardButton(
                        text="Reject", callback_data=f"reject:{msg.id}"
                    ),
                ]
            ]
        )
        for admin_id in settings.ADMIN_IDS:
            text = f"New message #{msg.id} from user {msg.user_id}: {msg.text}"
            await message.bot.send_message(
                chat_id=admin_id, text=text, reply_markup=keyboard
            )
        await message.answer(
            "Your message has been received with ID "
            f"{msg.id}. You can check status via /status {msg.id}."
        )
