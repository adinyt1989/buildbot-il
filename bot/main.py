import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from core.config import settings
from bot.handlers import auth

bot = Bot(token=settings.TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация обработчиков
auth.register_handlers(dp)

async def main():
    await dp.start_polling()

if name == "main":
    asyncio.run(main())
