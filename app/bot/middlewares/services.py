from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any

from app.db.repositories.LogsRepository import LogsRepository
from app.db.repositories.SiteRepository import SiteRepository
from app.db.repositories.UserReposirory import UserRepository
from app.services.LogsService import LogsService
from app.services.SiteService import SiteService
from app.services.UserService import UserService
from app.monitoring.BackgroundResponses import BackgroundResponses

class ServiceMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker, checker: BackgroundResponses):
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
            logs_repo = LogsRepository(session)
            site_service = SiteService(site_repo, self.checker)

            #DI
            data["logs_service"] = LogsService(logs_repo)
            data["site_service"] = site_service
            data["user_service"] = UserService(user_repo)

            return await handler(event, data)