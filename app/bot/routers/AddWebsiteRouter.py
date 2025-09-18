from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.bot.routers.BaseRouter import BaseRouter
from app.bot.states.AddWebsiteState import AddSite


class AddWebSiteRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def _register_handlers(self):
        self.router.message(F.text=="Добавить сайт")(self.add_site_start_message)
        self.router.message(AddSite.waiting_for_url)(self.process_url)
        self.router.message(AddSite.waiting_for_interval)(self.process_interval)


    async def add_site_start_message(self, message: Message, state: FSMContext):
        await message.answer("Следующим сообщением отправьте URL веб-сайта:", reply_markup=ReplyKeyboardRemove())
        await state.set_state(AddSite.waiting_for_url)


    async def process_url(self,message: Message, state: FSMContext):
        await state.update_data(url=message.text)
        await message.answer("Введите интервал проверки (в минутах):")
        await state.set_state(AddSite.waiting_for_interval)


    async def process_interval(self,message: Message, state: FSMContext):
        interval = message.text

        if not message.text.isnumeric():
            await message.answer("Время должно быть указано числом!")
            return

        if int(interval)<=0:
            await message.answer("Время должно быть > 0")
            return

        data = await state.get_data()

        url = data["url"]

        await message.answer(f"Сайт {url} добавлен с интервалом {interval} минут")

        await state.clear()
