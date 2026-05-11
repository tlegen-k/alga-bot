import asyncio
import logging

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN, DATABASE_URL
from bot.db.connection import close_pool
from bot.db.leads import init_db
from bot.handlers.inquiry import router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


async def run_bot() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    if DATABASE_URL:
        await init_db()

    try:
        await dp.start_polling(bot)
    finally:
        await close_pool()
        await bot.session.close()


async def main() -> None:
    api_config = uvicorn.Config("bot.api:app", host="127.0.0.1", port=8000, log_level="info")
    api_server = uvicorn.Server(api_config)
    await asyncio.gather(
        run_bot(),
        api_server.serve(),
    )


if __name__ == "__main__":
    asyncio.run(main())
