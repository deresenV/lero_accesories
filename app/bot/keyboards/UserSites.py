from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.db.models import Site


def user_sites_inline(sites: list[Site]) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=site.url,
                                     callback_data=f"site:{site.id}")]
               for site in sites]
    return InlineKeyboardMarkup(inline_keyboard=buttons)