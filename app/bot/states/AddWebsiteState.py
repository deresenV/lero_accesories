from aiogram.fsm.state import StatesGroup, State


class AddSite(StatesGroup):
    waiting_for_url = State()
    waiting_for_interval = State()