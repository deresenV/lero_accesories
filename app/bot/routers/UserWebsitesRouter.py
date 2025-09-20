from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import F
from app.bot.keyboards.SiteKeyboards import site_info_keyboard, edit_site_keyboard, remove_site_keyboard, \
    history_keyboard, back_statistic_keyboard
from app.bot.keyboards.StartKeyboard import start_keyboard
from app.bot.keyboards.UserSites import user_sites_inline
from app.bot.routers.BaseRouter import BaseRouter
from app.bot.states.EditWebsiteState import EditSite
from app.services.LogsService import LogsService
from app.services.SiteService import SiteService
from app.services.UserService import UserService


class UserWebsitesRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def _register_handlers(self):
        #TODO рефакторинг роутеров на логические группы
        self.router.message(F.text == "Мои сайты")(self.user_websites)
        self.router.callback_query(F.data.startswith("back_to_my_sites"))(self.back_to_sites)
        self.router.callback_query(F.data.startswith("site:"))(self.website_info)
        self.router.callback_query(F.data.startswith("edit_site:"))(self.edit_site)

        self.router.callback_query(F.data.startswith("edit_site_url:"))(self.edit_site_url)
        self.router.callback_query(F.data.startswith("edit_site_interval:"))(self.edit_site_interval)

        self.router.message(EditSite.update_data)(self.process_update_data)
        self.router.callback_query(F.data.startswith("delete_site:"))(self.remove_site_process)
        self.router.callback_query(F.data.startswith("delete_site_succesful:"))(self.remove_site_succesful)
        self.router.callback_query(F.data.startswith("history_site:"))(self.history_site)
        self.router.callback_query(F.data.startswith("site_stats:"))(self.site_stats)
        self.router.callback_query(F.data.startswith("download_log:"))(self.download_log)
        self.router.callback_query(F.data.startswith("get_graphic:"))(self.get_site_stats_graphic)

    async def user_websites(self, message: Message, user_service: UserService):
        """Получение сайтов пользователя"""
        sites = await user_service.get_user_sites(message.from_user.id)

        if sites:
            await message.answer("Мои сайты:", reply_markup=user_sites_inline(sites))
        else:
            await message.answer("У вас нет сайтов", reply_markup=start_keyboard)

    async def back_to_sites(self, query: CallbackQuery, user_service: UserService):
        """callback возврат на сайты пользователя"""
        sites = await user_service.get_user_sites(query.from_user.id)

        if sites:
            await query.message.edit_text("Мои сайты:", reply_markup=user_sites_inline(sites))
        else:
            await query.message.edit_text("У вас нет сайтов", reply_markup=start_keyboard)

        await query.answer()


    async def website_info(self, query: CallbackQuery, site_service: SiteService):
        """Основная информация сайта"""
        site_id = int(query.data.split(":")[1])
        site = await site_service.get_site_by_id(site_id)
        await query.message.edit_text(f"URL: {site.url}\nЧастота опроса: Каждые {site.check_interval} минут", reply_markup=site_info_keyboard(site_id))
        await query.answer()


    async def edit_site(self, query: CallbackQuery):
        """Редактирование параметров сайта"""
        site_id = int(query.data.split(":")[1])
        await query.message.edit_text(f"Режим редактрирования", reply_markup=edit_site_keyboard(site_id))
        await query.answer()


    async def edit_site_url(self, query: CallbackQuery, state: FSMContext):
        """Редактирование url"""
        site_id = int(query.data.split(":")[1])
        await state.update_data(id=site_id)
        await state.update_data(type="url")
        await query.message.edit_text(f"Введите новый url")
        await state.set_state(EditSite.update_data)


    async def edit_site_interval(self, query: CallbackQuery, state: FSMContext):
        """Редактирование интервала опроса"""
        site_id = int(query.data.split(":")[1])
        await state.update_data(id=site_id)
        await state.update_data(type="interval")
        await query.message.edit_text(f"Введите новый интервал проверки")
        await query.answer()
        await state.set_state(EditSite.update_data)

    async def process_update_data(self, message: Message, state: FSMContext, site_service: SiteService):
        """Обновление и валидация данных"""
        data = await state.get_data()
        type = data["type"]
        update_data = message.text
        if type == "interval":
            try:
                interval = int(update_data)
            except ValueError:
                await message.answer("Время должно быть указано числом!")
                return

            if interval <= 0:
                await message.answer("Время должно быть > 0")
                return

        site_id = int(data["id"])
        site = await site_service.edit_data(type, site_id, update_data)
        await message.answer(f"URL: {site.url}\nЧастота опроса: Каждые {site.check_interval} минут",
                             reply_markup=site_info_keyboard(site_id))

    async def remove_site_process(self, query: CallbackQuery):
        """Защита от случайного удаления сайта"""
        site_id = int(query.data.split(":")[1])
        await query.message.edit_text(text="Удалить сайт?", reply_markup=remove_site_keyboard(site_id))
        await query.answer()

    async def remove_site_succesful(self, query: CallbackQuery, site_service: SiteService):
        """Удаление сайта"""
        site_id = int(query.data.split(":")[1])
        answer = await site_service.delete_site(site_id)
        await query.message.edit_text(text=answer)
        await query.answer()


    async def site_stats(self, query: CallbackQuery, logs_service: LogsService):
        """Статистика сайта"""
        site_id = int(query.data.split(":")[1])
        uptime, downtime, total = await logs_service.get_all_statistic(query.from_user.id, site_id)
        try:
            total = int(total)
            text_statistic = f"Статистика сайта:\nUptime: {uptime}%\nDowntime: {downtime}%\nВсего проверок: {total}"
        except:
            text_statistic = "Статистики нет"

        await query.message.edit_text(text=text_statistic, reply_markup=back_statistic_keyboard(site_id))


    async def get_site_stats_graphic(self, query: CallbackQuery, logs_service: LogsService):
        site_id = int(query.data.split(":")[1])
        file = await logs_service.site_stats_graphic(query.from_user.id, site_id)
        if not file:
            await query.message.answer("Нет данных для графика.")
            return

        await query.message.answer_photo(
            photo=FSInputFile(file),
            caption="Статистика доступности и времени ответа",
        )
        await query.answer()


    async def history_site(self, query: CallbackQuery, logs_service: LogsService):
        """История опроса сайта"""
        site_id = int(query.data.split(":")[1])

        text_log = await logs_service.get_all_log_by_user_site(query.from_user.id, site_id)

        history_text = "История опроса сайта(Последние 10 опросов):\n\n" + "\n".join(text_log[-10:])

        await query.message.edit_text(text=history_text, reply_markup=history_keyboard(site_id))
        await query.answer()

    async def download_log(self, query: CallbackQuery, logs_service: LogsService):
        """Скачать историю сайта"""
        site_id = int(query.data.split(":")[1])

        file = await logs_service.format_log_for_file(query.from_user.id, site_id)
        await query.message.answer_document(file)
        await query.answer()