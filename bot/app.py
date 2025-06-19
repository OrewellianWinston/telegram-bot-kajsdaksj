"""Application entrypoint combining FastAPI and Aiogram."""

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from .config import settings
from .handlers.user_handlers import register_user_handlers
from .handlers.admin_handlers import register_admin_handlers


BOT_TOKEN = settings.BOT_TOKEN
WEBHOOK_PATH = "/webhook"
WEBHOOK_URL = WEBHOOK_PATH  # In production, full URL should be provided

app = FastAPI()

storage = RedisStorage2.from_url(settings.REDIS_URL)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)

register_user_handlers(dp)
register_admin_handlers(dp)


@app.on_event("startup")
async def on_startup() -> None:
    await bot.set_webhook(WEBHOOK_URL)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    await bot.delete_webhook()
    await storage.close()


@app.post(WEBHOOK_PATH)
async def telegram_webhook(req: Request) -> None:
    data = await req.json()
    update = types.Update.to_object(data)
    await dp.process_update(update)
