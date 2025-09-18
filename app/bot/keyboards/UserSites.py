from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def user_sites(sites):
    keyboard = [[KeyboardButton(text=site.url)] for site in sites]  # <-- берем url
    user_sites_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
    return user_sites_keyboard