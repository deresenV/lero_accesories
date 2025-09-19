import asyncio
from aiogram import Bot, Dispatcher

from app.config import settings
from app.bot.routers import routers
from app.bot.middlewares.services import ServiceMiddleware
from app.db.database import create_tables, AsyncSessionLocal
from app.db.repositories.LogsRepository import LogsRepository
from app.db.repositories.SiteRepository import SiteRepository
from app.monitoring.BackgroundTask import BackgroundTask
from app.monitoring.SiteChecker import SiteChecker
from app.services.LogsService import LogsService
from app.services.NotifyService import NotifyService
from app.services.SiteService import SiteService

dp = Dispatcher()

async def main() -> None:
    await create_tables()
    bot = Bot(token=settings.bot_token)
    dp.include_router(routers)

    checker = BackgroundTask()
    notify_service = NotifyService(bot=bot)
    site_checker = SiteChecker()
    async with AsyncSessionLocal() as session:
        site_repo = SiteRepository(session)
        site_service = SiteService(site_repo, checker)
        checker.set_service(site_service)
        checker.notify_service = notify_service
        checker.site_checker = site_checker
        logs_repo = LogsRepository(session)
        checker.logs_service = LogsService(logs_repo)

    dp.update.middleware(ServiceMiddleware(AsyncSessionLocal, checker))

    await checker.load_sites()
    asyncio.create_task(checker.run())

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
