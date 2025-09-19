from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any

from app.db.repositories.SiteRepository import SiteRepository
from app.db.repositories.UserReposirory import UserRepository
from app.services.SiteService import SiteService
from app.services.UserService import UserService
from app.monitoring.BackgroundTask import BackgroundTask

class ServiceMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker, checker: BackgroundTask):
        self.sessionmaker = sessionmaker
        self.checker = checker

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        async with self.sessionmaker() as session:
            user_repo = UserRepository(session)
            site_repo = SiteRepository(session)

            site_service = SiteService(site_repo, self.checker)

            data["site_service"] = site_service
            data["user_service"] = UserService(user_repo)

            return await handler(event, data)