from aiogram.types import Message
from aiogram import F

from app.bot.keyboards.UserSites import user_sites
from app.bot.routers.BaseRouter import BaseRouter
from app.services.UserService import UserService


class UserWebsitesRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def _register_handlers(self):
        self.router.message(F.text == "Мои сайты")(self.user_websites)


    async def user_websites(self, message: Message, user_service: UserService):
        sites = await user_service.get_user_sites(message.from_user.id)

        await message.answer("Мои сайты:", reply_markup=user_sites(sites))