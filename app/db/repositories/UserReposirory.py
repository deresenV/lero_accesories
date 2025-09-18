from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from app.db.models import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Получает пользователя по ID без сайтов"""
        return await self.session.get(User, user_id)

    async def get_user_with_sites(self, user_id: int) -> User | None:
        """Получает пользователя с предзагруженными сайтами"""
        result = await self.session.execute(
            select(User)
            .options(selectinload(User.sites))  # загружаем сайты сразу
            .where(User.telegram_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, user_id: int) -> User:
        """Создает нового пользователя"""
        user = User(telegram_id=user_id)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)  # обновляем объект после коммита
        return user