from aiogram.fsm.state import StatesGroup, State


class EditSite(StatesGroup):
    update_data = State()