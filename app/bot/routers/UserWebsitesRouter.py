from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import F

from app.bot.keyboards.SiteKeyboards import site_info_keyboard, edit_site_keyboard, remove_site_keyboard
from app.bot.keyboards.StartKeyboard import start_keyboard
from app.bot.keyboards.UserSites import user_sites_inline
from app.bot.routers.BaseRouter import BaseRouter
from app.bot.states.EditWebsiteState import EditSite
from app.services.SiteService import SiteService
from app.services.UserService import UserService


class UserWebsitesRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def _register_handlers(self):
        self.router.message(F.text == "Мои сайты")(self.user_websites)
        self.router.callback_query(F.data.startswith("back_to_my_sites"))(self.back_to_sites)
        self.router.callback_query(F.data.startswith("site:"))(self.website_info)
        self.router.callback_query(F.data.startswith("edit_site:"))(self.edit_site)

        self.router.callback_query(F.data.startswith("edit_site_url:"))(self.edit_site_url)
        self.router.callback_query(F.data.startswith("edit_site_interval:"))(self.edit_site_interval)

        self.router.message(EditSite.update_data)(self.process_update_data)
        self.router.callback_query(F.data.startswith("delete_site:"))(self.remove_site_process)
        self.router.callback_query(F.data.startswith("delete_site_succesful:"))(self.remove_site_succesful)

    async def user_websites(self, message: Message, user_service: UserService):
        sites = await user_service.get_user_sites(message.from_user.id)

        if sites:
            await message.answer("Мои сайты:", reply_markup=user_sites_inline(sites))
        else:
            await message.answer("У вас нет сайтов", reply_markup=start_keyboard)

    async def back_to_sites(self, query: CallbackQuery, user_service: UserService):
        sites = await user_service.get_user_sites(query.from_user.id)

        if sites:
            await query.message.edit_text("Мои сайты:", reply_markup=user_sites_inline(sites))
        else:
            await query.message.edit_text("У вас нет сайтов", reply_markup=start_keyboard)

        await query.answer()


    async def website_info(self, query: CallbackQuery, site_service: SiteService):
        site_id = int(query.data.split(":")[1])
        site = await site_service.get_site_by_id(site_id)
        await query.message.edit_text(f"URL: {site.url}\nЧастота опроса: Каждые {site.check_interval} минут", reply_markup=site_info_keyboard(site_id))


    async def edit_site(self, query: CallbackQuery):
        site_id = int(query.data.split(":")[1])
        await query.message.edit_text(f"Режим редактрирования", reply_markup=edit_site_keyboard(site_id))


    async def edit_site_url(self, query: CallbackQuery, state: FSMContext):
        site_id = int(query.data.split(":")[1])
        await state.update_data(id=site_id)
        await state.update_data(type="url")
        await query.message.edit_text(f"Введите новый url")
        await state.set_state(EditSite.update_data)

    async def process_update_data(self, message: Message, state: FSMContext, site_service: SiteService):
        update_data = message.text
        data = await state.get_data()
        site_id = int(data["id"])
        type = data["type"]
        site = await site_service.edit_data(type, site_id, update_data)
        await message.answer(f"URL: {site.url}\nЧастота опроса: Каждые {site.check_interval} минут", reply_markup=site_info_keyboard(site_id))


    async def edit_site_interval(self, query: CallbackQuery, state: FSMContext):
        site_id = int(query.data.split(":")[1])
        await state.update_data(id=site_id)
        await state.update_data(type="interval")
        await query.message.edit_text(f"Введите новый интервал проверки")
        await state.set_state(EditSite.update_data)

    async def remove_site_process(self, query: CallbackQuery):
        site_id = int(query.data.split(":")[1])
        await query.message.edit_text(text="Удалить сайт?", reply_markup=remove_site_keyboard(site_id))

    async def remove_site_succesful(self, query: CallbackQuery, site_service: SiteService):
        site_id = int(query.data.split(":")[1])
        answer = await site_service.delete_site(site_id)
        await query.message.edit_text(text=answer)
