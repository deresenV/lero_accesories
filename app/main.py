import asyncio
from aiogram import Bot, Dispatcher

from app.config import settings
from app.bot.routers import routers
from app.bot.middlewares.services import ServiceMiddleware
from app.db.database import create_tables, AsyncSessionLocal
from app.db.repositories.LogsRepository import LogsRepository
from app.db.repositories.SiteRepository import SiteRepository
from app.monitoring.BackgroundResponses import BackgroundResponses
from app.monitoring.SiteChecker import SiteChecker
from app.services.LogsService import LogsService
from app.services.NotifyService import NotifyService
from app.services.SiteService import SiteService

dp = Dispatcher()

async def main() -> None:
    await create_tables()
    bot = Bot(token=settings.bot_token)
    dp.include_router(routers)

    background_responses_monitoring = BackgroundResponses() # Фоновый мониторинг сайтов
    notify_service = NotifyService(bot=bot) # Сервис уведомлений
    site_checker = SiteChecker()  # Модуль опроса сайтов

    #Сессия для мониторинга
    async with AsyncSessionLocal() as session:
        site_repo = SiteRepository(session)
        site_service = SiteService(site_repo, background_responses_monitoring)
        background_responses_monitoring.set_service(site_service)
        background_responses_monitoring.notify_service = notify_service
        background_responses_monitoring.site_checker = site_checker
        logs_repo = LogsRepository(session)
        background_responses_monitoring.logs_service = LogsService(logs_repo)


    dp.update.middleware(ServiceMiddleware(AsyncSessionLocal, background_responses_monitoring))

    await background_responses_monitoring.load_sites() #Подгрузка сайтов из бд в очередь опроса
    asyncio.create_task(background_responses_monitoring.run())

    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
