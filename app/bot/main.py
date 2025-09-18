import asyncio

from app.bot.middlewares.services import ServiceMiddleware
from app.bot.routers import routers
from app.config import settings
from aiogram import Bot, Dispatcher

from app.db.database import create_tables, AsyncSessionLocal

dp = Dispatcher()

async def main() -> None:
    await create_tables()
    bot = Bot(token=settings.bot_token)
    dp.include_router(routers)
    dp.update.middleware(ServiceMiddleware(AsyncSessionLocal))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())