from app.bot.keyboards.CancelKeyboard import cancel_kb
from app.bot.keyboards.StartKeyboard import start_keyboard
from app.bot.routers.BaseRouter import BaseRouter
from app.bot.states.AddWebsiteState import AddSite

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram import F

class AddWebSiteRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def _register_handlers(self):
        """Регистрация хендлеров"""
        self.router.message(F.text=="Добавить сайт")(self.add_site_start_message)
        self.router.message(AddSite.waiting_for_url)(self.process_url)
        self.router.message(AddSite.waiting_for_interval)(self.process_interval)


    async def add_site_start_message(self, message: Message, state: FSMContext):
        """
        1 stage
        Старт state context
        """
        await message.answer("Следующим сообщением отправьте URL веб-сайта:", reply_markup=cancel_kb)
        await state.set_state(AddSite.waiting_for_url)


    async def process_url(self,message: Message, state: FSMContext):
        """
        2 stage
        Считывание и запись url | Отмена
        """
        url = message.text
        if url == "Отмена":
            await state.clear()
            await message.answer("Отменено", reply_markup=start_keyboard)
            return


        await state.update_data(url=url)
        await message.answer("Введите интервал проверки (в минутах):", reply_markup=cancel_kb)
        await state.set_state(AddSite.waiting_for_interval)


    async def process_interval(self, message: Message, state: FSMContext):
        """
        3 stage
        Считывание, проверка и запись интервала опроса сервера | Отмена
        """
        interval = message.text
        if interval == "Отмена":
            await state.clear()
            await message.answer("Отменено", reply_markup=start_keyboard)
            return

        try:
            interval = int(message.text)
        except ValueError:
            await message.answer("Время должно быть указано числом!", reply_markup=cancel_kb)
            return

        if interval <= 0:
            await message.answer("Время должно быть > 0", reply_markup=cancel_kb)
            return

        data = await state.get_data()

        url = data["url"]


        await message.answer(f"Сайт {url} добавлен с интервалом {interval} минут")

        await state.clear()
