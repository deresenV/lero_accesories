from app.db.models import User


class UserRepository:
    def __init__(self, session):
        self.session = session

    async def get_user_by_id(self, user_id: str):
        return await self.session.get(User, user_id)

    async def create_user(self, user_id: int):
        user = User(telegram_id=user_id)
        self.session.add(user)
        await self.session.commit()
        return user