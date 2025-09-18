from app.db.repositories.UserReposirory import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def get_or_create_user(self, user_id: int):
        user = await self.user_repo.get_user_by_id(user_id)
        if not user:
            user = await self.user_repo.create_user(user_id)
        return user

