"""Service responsible for publishing approved messages."""

from aiogram import Bot

from ..config import settings


async def publish_to_channel(bot: Bot, text: str) -> None:
    """Send approved text to configured channel."""
    await bot.send_message(chat_id=settings.CHANNEL_ID, text=text)
