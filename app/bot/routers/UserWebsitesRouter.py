from aiogram.types import Message
from aiogram import F

from app.bot.routers.BaseRouter import BaseRouter


class UserWebsitesRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def _register_handlers(self):
        self.router.message(F.text == "Мои сайты")(self.user_websites)


    async def user_websites(self, message: Message):
        await message.answer("Мои сайты:")