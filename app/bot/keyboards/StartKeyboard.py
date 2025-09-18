from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить сайт")],
        [KeyboardButton(text="Мои сайты")],
    ],
    resize_keyboard=True
)
