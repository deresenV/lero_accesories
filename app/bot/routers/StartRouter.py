from aiogram.types import Message
from aiogram.filters import Command

from app.bot.keyboards.StartKeyboard import start_keyboard
from app.bot.routers.BaseRouter import BaseRouter
from app.services.UserService import UserService


class StartRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def _register_handlers(self):
        self.router.message(Command("start"))(self.start_command)


    async def start_command(self,
                            message: Message,
                            user_service: UserService):
        user = await user_service.get_or_create_user(message.from_user.id)
        await message.answer("Воспользуйтесь меню для продолжения", reply_markup=start_keyboard)