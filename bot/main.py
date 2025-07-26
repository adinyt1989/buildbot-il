import asyncio
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from core.config import settings
from bot.handlers import auth, orders, payments, profile

bot = Bot(token=settings.TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Регистрация обработчиков
auth.register_handlers(dp)
orders.register_handlers(dp)
payments.register_handlers(dp)
profile.register_handlers(dp)

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    asyncio.run(main())
