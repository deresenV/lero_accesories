from aiogram.types import Message
from aiogram.filters import Command

from app.bot.keyboards.StartKeyboard import start_keyboard
from app.bot.routers.BaseRouter import BaseRouter


class StartRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def _register_handlers(self):
        self.router.message(Command("start"))(self.start_command)


    async def start_command(self, message: Message):
        await message.answer("Воспользуйтесь меню для продолжения", reply_markup=start_keyboard)