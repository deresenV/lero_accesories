from aiogram import BaseMiddleware
from typing import Callable, Awaitable, Dict, Any

from app.db.repositories.SiteRepository import SiteRepository
from app.db.repositories.UserReposirory import UserRepository
from app.services.SiteService import SiteService
from app.services.UserService import UserService


class ServiceMiddleware(BaseMiddleware):
    def __init__(self, sessionmaker):
        self.sessionmaker = sessionmaker

    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any],
    ) -> Any:
        async with self.sessionmaker() as session:
            user_repo = UserRepository(session)
            site_repo = SiteRepository(session)

            data["site_service"] = SiteService(site_repo)
            data["user_service"] = UserService(user_repo)

            return await handler(event, data)
