import asyncio

from app.bot.routers import routers
from app.config import settings
from aiogram import Bot, Dispatcher

dp = Dispatcher()

async def main() -> None:
    bot = Bot(token=settings.bot_token)
    dp.include_router(routers)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())